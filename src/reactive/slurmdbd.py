import subprocess

from charms.reactive import (
    endpoint_from_flag,
    set_flag,
    when,
    when_not,
)

from charmhelpers.core.hookenv import (
    open_port,
    unit_private_ip,
    status_set,
    log,
)


@when('slurm.base.available')
@when_not('snap.mode.set')
def set_snap_mode():
    """Set the snap.mode to slurmdbd
    """
    if subprocess.call(["snap", "set", "slurm", "snap.mode=slurmdbd"]) == 0:
        open_port(6819)
        status_set("active", f"slurmdbd available")
        set_flag('slurm.snap.mode.set')
    else:
        msg = "DEBUG NEEDED - set_snap_mode()"
        status_set('blocked', msg)
        log(msg)
        return


@when('snap.mode.set',
      'endpoint.slurmdbd-host-port.joined')
def provide_http_relation_data():
    endpoint = endpoint_from_flag('endpoint.slurmdbd.host-port.joined')
    status_set('maintenance', "Sending host:port to requirer ...")
    endpoint.configure(
        host=unit_private_ip(),
        port="6819"
    )

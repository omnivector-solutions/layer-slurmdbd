from subprocess import check_output

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
)


@when('slurm.base.available')
@when_not('slurm.snap.mode.set')
def set_snap_mode():
    """Set the snap.mode to slurmdbd
    """
    out = check_output(["snap", "set", "slurm", "snap.mode=slurmdbd"])
    if out:
        open_port(6819)
        status_set("active", f"slurmdbd available")
        set_flag('slurm.snap.mode.set')
    else:
        status_set('blocked', "DEBUG_SNAP_MODE_SET")
        return

@when('slurm.snap.mode.set',
      'endpoint.slurmdbd-host-port.joined')
def provide_http_relation_data():
    endpoint = endpoint_from_flag('endpoint.slurmdbd.host-port.joined')
    status_set('maintenance', "Sending host:port to requirer ...")
    endpoint.configure(
        host=unit_private_ip(),
        port="6819"
    )

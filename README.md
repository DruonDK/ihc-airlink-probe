# IHC Airlink Probe

Temporary, read-only diagnostic for the IHC custom integration
(dingusdk/haihc-betatest). Adds the service `ihc_airlink_probe.airlink_dump`,
which calls `AirlinkManagementService.getDetectedDeviceList` on every loaded
IHC controller and returns battery level, signal strength, serial number,
device type and version for each wireless (Airlink) device.

Uses the controller connection the IHC integration already has. Changes nothing.

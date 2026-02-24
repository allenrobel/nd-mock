# Nexus Dashboard Object Hierarchy

## Hierarchy Chain

`Fabric Group (MSD) > Fabric > VRF > Network > Switch > Interface`

Top-down policy deployment: global settings at Fabric level → VRF segmentation (L3 overlay) → Network partitions (L2) → pushed to physical switches.

## Object Definitions

| Object | Level | Purpose |
| --- | --- | --- |
| Fabric Group / MSD | Top | Manages multiple fabrics and inter-site connectivity |
| Fabric | 1 | Logical container (e.g., VXLAN BGP EVPN); represents a physical site/DC |
| VRF | 2 | Virtual Routing & Forwarding; L3 overlay segmentation within fabric |
| Network / Bridge Domain | 3 | Subset of VRF; defines VLANs and subnet connectivity (L2) |
| Switch (Leaf/Spine) | 4 | Physical device where configurations are deployed |
| Interface | 5 | Physical port (access, trunk, port-channel) on switch |

## Object Relationships

- Networks must belong to a VRF
- VRFs must reside in a Fabric
- Switches are added to Fabrics
- VRFs and Networks inherit down to switches when attached
- Configurations are pushed from Fabric → Switch interfaces

## Constraints

| Object | Constraint |
| --- | --- |
| Any | Cannot create if already exists |
| Fabric | Cannot modify if in read_only mode |
| Fabric | Cannot delete if contains switches |
| VRF | Cannot delete if attached to switches |
| Network | Cannot delete if attached to switches |

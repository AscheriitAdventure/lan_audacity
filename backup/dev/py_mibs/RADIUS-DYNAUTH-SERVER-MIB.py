#
# PySNMP MIB module RADIUS-DYNAUTH-SERVER-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/RADIUS-DYNAUTH-SERVER-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:25:42 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, Integer, OctetString, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "Integer", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, ValueSizeConstraint, SingleValueConstraint, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "ValueSizeConstraint", "SingleValueConstraint", "ValueRangeConstraint")
( InetAddress, InetAddressType, ) = mibBuilder.importSymbols("INET-ADDRESS-MIB", "InetAddress", "InetAddressType")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( NotificationGroup, ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance", "ObjectGroup")
( iso, Unsigned32, MibIdentifier, mib_2, ObjectIdentity, TimeTicks, ModuleIdentity, Bits, Gauge32, Integer32, Counter64, Counter32, NotificationType, IpAddress, MibScalar, MibTable, MibTableRow, MibTableColumn, ) = mibBuilder.importSymbols("SNMPv2-SMI", "iso", "Unsigned32", "MibIdentifier", "mib-2", "ObjectIdentity", "TimeTicks", "ModuleIdentity", "Bits", "Gauge32", "Integer32", "Counter64", "Counter32", "NotificationType", "IpAddress", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
radiusDynAuthServerMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 146)).setRevisions(("2006-08-29 00:00",))
if mibBuilder.loadTexts: radiusDynAuthServerMIB.setLastUpdated('200608290000Z')
if mibBuilder.loadTexts: radiusDynAuthServerMIB.setOrganization('IETF RADEXT Working Group')
if mibBuilder.loadTexts: radiusDynAuthServerMIB.setContactInfo(" Stefaan De Cnodder\n                Alcatel\n                Francis Wellesplein 1\n                B-2018 Antwerp\n                Belgium\n\n                Phone: +32 3 240 85 15\n                EMail: stefaan.de_cnodder@alcatel.be\n\n                Nagi Reddy Jonnala\n                Cisco Systems, Inc.\n                Divyasree Chambers, B Wing,\n                O'Shaugnessy Road,\n                Bangalore-560027, India.\n\n                Phone: +91 94487 60828\n                EMail: njonnala@cisco.com\n\n                Murtaza Chiba\n                Cisco Systems, Inc.\n                170 West Tasman Dr.\n                San Jose CA, 95134\n\n                Phone: +1 408 525 7198\n                EMail: mchiba@cisco.com ")
if mibBuilder.loadTexts: radiusDynAuthServerMIB.setDescription('The MIB module for entities implementing the server\n            side of the Dynamic Authorization Extensions to the\n            Remote Authentication Dial-In User Service (RADIUS)\n            protocol.  Copyright (C) The Internet Society (2006).\n\n\n\n            Initial version as published in RFC 4673; for full\n            legal notices see the RFC itself.')
radiusDynAuthServerMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 1))
radiusDynAuthServerScalars = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 1, 1))
radiusDynAuthServerDisconInvalidClientAddresses = MibScalar((1, 3, 6, 1, 2, 1, 146, 1, 1, 1), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServerDisconInvalidClientAddresses.setDescription('The number of Disconnect-Request packets received from\n             unknown addresses.  This counter may experience a\n             discontinuity when the DAS module (re)starts, as\n             indicated by the value of\n             radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServerCoAInvalidClientAddresses = MibScalar((1, 3, 6, 1, 2, 1, 146, 1, 1, 2), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServerCoAInvalidClientAddresses.setDescription('The number of CoA-Request packets received from unknown\n             addresses.  This counter may experience a discontinuity\n             when the DAS module (re)starts, as indicated by the\n             value of radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServerIdentifier = MibScalar((1, 3, 6, 1, 2, 1, 146, 1, 1, 3), SnmpAdminString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServerIdentifier.setDescription('The NAS-Identifier of the RADIUS Dynamic Authorization\n              Server.  This is not necessarily the same as sysName in\n              MIB II.')
radiusDynAuthClientTable = MibTable((1, 3, 6, 1, 2, 1, 146, 1, 2), )
if mibBuilder.loadTexts: radiusDynAuthClientTable.setDescription('The (conceptual) table listing the RADIUS Dynamic\n             Authorization Clients with which the server shares a\n             secret.')
radiusDynAuthClientEntry = MibTableRow((1, 3, 6, 1, 2, 1, 146, 1, 2, 1), ).setIndexNames((0, "RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthClientIndex"))
if mibBuilder.loadTexts: radiusDynAuthClientEntry.setDescription('An entry (conceptual row) representing one Dynamic\n              Authorization Client with which the server shares a\n              secret.')
radiusDynAuthClientIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1,2147483647)))
if mibBuilder.loadTexts: radiusDynAuthClientIndex.setDescription('A number uniquely identifying each RADIUS Dynamic\n              Authorization Client with which this Dynamic\n              Authorization Server communicates.  This number is\n              allocated by the agent implementing this MIB module\n              and is unique in this context.')
radiusDynAuthClientAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 2), InetAddressType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthClientAddressType.setDescription('The type of IP address of the RADIUS Dynamic\n              Authorization Client referred to in this table entry.')
radiusDynAuthClientAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 3), InetAddress()).setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthClientAddress.setDescription('The IP address value of the RADIUS Dynamic\n              Authorization Client referred to in this table entry,\n              using the version neutral IP address format.  The type\n              of this address is determined by the value of\n              the radiusDynAuthClientAddressType object.')
radiusDynAuthServDisconRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 4), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconRequests.setDescription("The number of RADIUS Disconnect-Requests received\n              from this Dynamic Authorization Client.  This also\n              includes the RADIUS Disconnect-Requests that have a\n              Service-Type attribute with value 'Authorize Only'.\n              This counter may experience a discontinuity when the\n\n\n\n              DAS module (re)starts as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconAuthOnlyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 5), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconAuthOnlyRequests.setDescription("The number of RADIUS Disconnect-Requests that include\n              a Service-Type attribute with value 'Authorize Only'\n              received from this Dynamic Authorization Client.  This\n              counter may experience a discontinuity when the DAS\n              module (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDupDisconRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 6), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDupDisconRequests.setDescription('The number of duplicate RADIUS Disconnect-Request\n              packets received from this Dynamic Authorization\n              Client.  This counter may experience a discontinuity\n              when the DAS module (re)starts, as indicated by the\n              value of radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServDisconAcks = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 7), Counter32()).setUnits('replies').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconAcks.setDescription('The number of RADIUS Disconnect-ACK packets sent to\n              this Dynamic Authorization Client.  This counter may\n              experience a discontinuity when the DAS module\n              (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServDisconNaks = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 8), Counter32()).setUnits('replies').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconNaks.setDescription("The number of RADIUS Disconnect-NAK packets\n              sent to this Dynamic Authorization Client.  This\n              includes the RADIUS Disconnect-NAK packets sent\n              with a Service-Type attribute with value 'Authorize\n              Only' and the RADIUS Disconnect-NAK packets sent\n              because no session context was found.  This counter\n              may experience a discontinuity when the DAS module\n              (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconNakAuthOnlyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 9), Counter32()).setUnits('replies').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconNakAuthOnlyRequests.setDescription("The number of RADIUS Disconnect-NAK packets that\n              include a Service-Type attribute with value\n              'Authorize Only' sent to this Dynamic Authorization\n              Client.  This counter may experience a discontinuity\n              when the DAS module (re)starts, as indicated by the\n              value of radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDisconNakSessNoContext = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 10), Counter32()).setUnits('replies').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconNakSessNoContext.setDescription('The number of RADIUS Disconnect-NAK packets\n              sent to this Dynamic Authorization Client\n              because no session context was found.  This counter may\n\n\n\n              experience a discontinuity when the DAS module\n              (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServDisconUserSessRemoved = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 11), Counter32()).setUnits('sessions').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconUserSessRemoved.setDescription('The number of user sessions removed for the\n              Disconnect-Requests received from this\n              Dynamic Authorization Client.  Depending on site-\n              specific policies, a single Disconnect request\n              can remove multiple user sessions.  In cases where\n              this Dynamic Authorization Server has no\n              knowledge of the number of user sessions that\n              are affected by a single request, each such\n              Disconnect-Request will count as a single\n              affected user session only.  This counter may experience\n              a discontinuity when the DAS module (re)starts, as\n              indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServMalformedDisconRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 12), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServMalformedDisconRequests.setDescription('The number of malformed RADIUS Disconnect-Request\n              packets received from this Dynamic Authorization\n              Client.  Bad authenticators and unknown types are not\n              included as malformed Disconnect-Requests.  This counter\n              may experience a discontinuity when the DAS module\n              (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServDisconBadAuthenticators = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 13), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconBadAuthenticators.setDescription('The number of RADIUS Disconnect-Request packets\n              that contained an invalid Authenticator field\n              received from this Dynamic Authorization Client.  This\n              counter may experience a discontinuity when the DAS\n              module (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServDisconPacketsDropped = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 14), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDisconPacketsDropped.setDescription('The number of incoming Disconnect-Requests\n              from this Dynamic Authorization Client silently\n              discarded by the server application for some reason\n              other than malformed, bad authenticators, or unknown\n              types.  This counter may experience a discontinuity\n              when the DAS module (re)starts, as indicated by the\n              value of radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServCoARequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 15), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoARequests.setDescription("The number of RADIUS CoA-requests received from this\n              Dynamic Authorization Client.  This also includes\n              the CoA requests that have a Service-Type attribute\n              with value 'Authorize Only'.  This counter may\n              experience a discontinuity when the DAS module\n              (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoAAuthOnlyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 16), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoAAuthOnlyRequests.setDescription("The number of RADIUS CoA-requests that include a\n              Service-Type attribute with value 'Authorize Only'\n              received from this Dynamic Authorization Client.  This\n              counter may experience a discontinuity when the DAS\n              module (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServDupCoARequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 17), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServDupCoARequests.setDescription('The number of duplicate RADIUS CoA-Request packets\n              received from this Dynamic Authorization Client.  This\n              counter may experience a discontinuity when the DAS\n              module (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServCoAAcks = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 18), Counter32()).setUnits('replies').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoAAcks.setDescription('The number of RADIUS CoA-ACK packets sent to this\n              Dynamic Authorization Client.  This counter may\n              experience a discontinuity when the DAS module\n\n\n\n              (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServCoANaks = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 19), Counter32()).setUnits('replies').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoANaks.setDescription("The number of RADIUS CoA-NAK packets sent to\n              this Dynamic Authorization Client.  This includes\n              the RADIUS CoA-NAK packets sent with a Service-Type\n              attribute with value 'Authorize Only' and the RADIUS\n              CoA-NAK packets sent because no session context was\n              found.  This counter may experience a discontinuity\n              when the DAS module (re)starts, as indicated by the\n              value of radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoANakAuthOnlyRequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 20), Counter32()).setUnits('replies').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoANakAuthOnlyRequests.setDescription("The number of RADIUS CoA-NAK packets that include a\n              Service-Type attribute with value 'Authorize Only'\n              sent to this Dynamic Authorization Client.  This counter\n              may experience a discontinuity when the DAS module\n              (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServCoANakSessNoContext = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 21), Counter32()).setUnits('replies').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoANakSessNoContext.setDescription('The number of RADIUS CoA-NAK packets sent to this\n              Dynamic Authorization Client because no session context\n              was found.  This counter may experience a discontinuity\n              when the DAS module (re)starts, as indicated by the\n              value of radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServCoAUserSessChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 22), Counter32()).setUnits('sessions').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoAUserSessChanged.setDescription("The number of user sessions authorization\n              changed for the CoA-Requests received from this\n              Dynamic Authorization Client.  Depending on site-\n              specific policies, a single CoA request can change\n              multiple user sessions' authorization.  In cases where\n              this Dynamic Authorization Server has no knowledge of\n              the number of user sessions that are affected by a\n              single request, each such CoA-Request will\n              count as a single affected user session only.  This\n              counter may experience a discontinuity when the DAS\n              module (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.")
radiusDynAuthServMalformedCoARequests = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 23), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServMalformedCoARequests.setDescription('The number of malformed RADIUS CoA-Request packets\n              received from this Dynamic Authorization Client.  Bad\n              authenticators and unknown types are not included as\n              malformed CoA-Requests.  This counter may experience a\n              discontinuity when the DAS module (re)starts, as\n              indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServCoABadAuthenticators = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 24), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoABadAuthenticators.setDescription('The number of RADIUS CoA-Request packets that\n              contained an invalid Authenticator field received\n              from this Dynamic Authorization Client.  This counter\n              may experience a discontinuity when the DAS module\n              (re)starts, as indicated by the value of\n                radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServCoAPacketsDropped = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 25), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServCoAPacketsDropped.setDescription('The number of incoming CoA packets from this\n              Dynamic Authorization Client silently discarded\n              by the server application for some reason other than\n              malformed, bad authenticators, or unknown types.  This\n              counter may experience a discontinuity when the DAS\n              module (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServUnknownTypes = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 26), Counter32()).setUnits('requests').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServUnknownTypes.setDescription('The number of incoming packets of unknown types that\n              were received on the Dynamic Authorization port.  This\n              counter may experience a discontinuity when the DAS\n\n\n\n              module (re)starts, as indicated by the value of\n              radiusDynAuthServerCounterDiscontinuity.')
radiusDynAuthServerCounterDiscontinuity = MibTableColumn((1, 3, 6, 1, 2, 1, 146, 1, 2, 1, 27), TimeTicks()).setUnits('hundredths of a second').setMaxAccess("readonly")
if mibBuilder.loadTexts: radiusDynAuthServerCounterDiscontinuity.setDescription('The time (in hundredths of a second) since the\n              last counter discontinuity.  A discontinuity may\n              be the result of a reinitialization of the DAS\n              module within the managed entity.')
radiusDynAuthServerMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 2))
radiusDynAuthServerMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 2, 1))
radiusDynAuthServerMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 146, 2, 2))
radiusAuthServerMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 146, 2, 1, 1)).setObjects(*(("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerMIBGroup"),))
if mibBuilder.loadTexts: radiusAuthServerMIBCompliance.setDescription('The compliance statement for entities implementing\n              the RADIUS Dynamic Authorization Server.  Implementation\n              of this module is for entities that support IPv4 and/or\n              IPv6.')
radiusDynAuthServerMIBGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 146, 2, 2, 1)).setObjects(*(("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerDisconInvalidClientAddresses"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerCoAInvalidClientAddresses"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerIdentifier"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthClientAddressType"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthClientAddress"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDupDisconRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconAcks"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconNaks"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconUserSessRemoved"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServMalformedDisconRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconBadAuthenticators"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconPacketsDropped"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoARequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDupCoARequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoAAcks"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoANaks"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoAUserSessChanged"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServMalformedCoARequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoABadAuthenticators"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoAPacketsDropped"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServUnknownTypes"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServerCounterDiscontinuity"),))
if mibBuilder.loadTexts: radiusDynAuthServerMIBGroup.setDescription('The collection of objects providing management of\n              a RADIUS Dynamic Authorization Server.')
radiusDynAuthServerAuthOnlyGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 146, 2, 2, 2)).setObjects(*(("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconAuthOnlyRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconNakAuthOnlyRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoAAuthOnlyRequests"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoANakAuthOnlyRequests"),))
if mibBuilder.loadTexts: radiusDynAuthServerAuthOnlyGroup.setDescription("The collection of objects supporting the RADIUS\n              messages including Service-Type attribute with\n              value 'Authorize Only'.")
radiusDynAuthServerNoSessGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 146, 2, 2, 3)).setObjects(*(("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServDisconNakSessNoContext"), ("RADIUS-DYNAUTH-SERVER-MIB", "radiusDynAuthServCoANakSessNoContext"),))
if mibBuilder.loadTexts: radiusDynAuthServerNoSessGroup.setDescription('The collection of objects supporting the RADIUS\n              messages that are referring to non-existing sessions.')
mibBuilder.exportSymbols("RADIUS-DYNAUTH-SERVER-MIB", radiusDynAuthServCoAAcks=radiusDynAuthServCoAAcks, radiusDynAuthServerCounterDiscontinuity=radiusDynAuthServerCounterDiscontinuity, radiusDynAuthServerScalars=radiusDynAuthServerScalars, radiusDynAuthClientEntry=radiusDynAuthClientEntry, radiusAuthServerMIBCompliance=radiusAuthServerMIBCompliance, radiusDynAuthServerNoSessGroup=radiusDynAuthServerNoSessGroup, radiusDynAuthServCoAPacketsDropped=radiusDynAuthServCoAPacketsDropped, radiusDynAuthServCoAAuthOnlyRequests=radiusDynAuthServCoAAuthOnlyRequests, radiusDynAuthServDisconNakSessNoContext=radiusDynAuthServDisconNakSessNoContext, radiusDynAuthServDisconRequests=radiusDynAuthServDisconRequests, radiusDynAuthServCoAUserSessChanged=radiusDynAuthServCoAUserSessChanged, radiusDynAuthServCoANakAuthOnlyRequests=radiusDynAuthServCoANakAuthOnlyRequests, radiusDynAuthServCoANaks=radiusDynAuthServCoANaks, radiusDynAuthClientIndex=radiusDynAuthClientIndex, radiusDynAuthServerIdentifier=radiusDynAuthServerIdentifier, radiusDynAuthServUnknownTypes=radiusDynAuthServUnknownTypes, radiusDynAuthServerDisconInvalidClientAddresses=radiusDynAuthServerDisconInvalidClientAddresses, radiusDynAuthClientTable=radiusDynAuthClientTable, radiusDynAuthServCoABadAuthenticators=radiusDynAuthServCoABadAuthenticators, radiusDynAuthServerMIBGroup=radiusDynAuthServerMIBGroup, radiusDynAuthServDisconAcks=radiusDynAuthServDisconAcks, radiusDynAuthServDisconNaks=radiusDynAuthServDisconNaks, radiusDynAuthServDupCoARequests=radiusDynAuthServDupCoARequests, radiusDynAuthServerMIBConformance=radiusDynAuthServerMIBConformance, radiusDynAuthServDisconPacketsDropped=radiusDynAuthServDisconPacketsDropped, radiusDynAuthServMalformedDisconRequests=radiusDynAuthServMalformedDisconRequests, radiusDynAuthServerCoAInvalidClientAddresses=radiusDynAuthServerCoAInvalidClientAddresses, radiusDynAuthServerMIBGroups=radiusDynAuthServerMIBGroups, radiusDynAuthServerAuthOnlyGroup=radiusDynAuthServerAuthOnlyGroup, radiusDynAuthServCoARequests=radiusDynAuthServCoARequests, radiusDynAuthServerMIB=radiusDynAuthServerMIB, radiusDynAuthServerMIBObjects=radiusDynAuthServerMIBObjects, radiusDynAuthServDupDisconRequests=radiusDynAuthServDupDisconRequests, PYSNMP_MODULE_ID=radiusDynAuthServerMIB, radiusDynAuthServDisconUserSessRemoved=radiusDynAuthServDisconUserSessRemoved, radiusDynAuthServerMIBCompliances=radiusDynAuthServerMIBCompliances, radiusDynAuthServCoANakSessNoContext=radiusDynAuthServCoANakSessNoContext, radiusDynAuthServDisconNakAuthOnlyRequests=radiusDynAuthServDisconNakAuthOnlyRequests, radiusDynAuthServMalformedCoARequests=radiusDynAuthServMalformedCoARequests, radiusDynAuthClientAddressType=radiusDynAuthClientAddressType, radiusDynAuthClientAddress=radiusDynAuthClientAddress, radiusDynAuthServDisconAuthOnlyRequests=radiusDynAuthServDisconAuthOnlyRequests, radiusDynAuthServDisconBadAuthenticators=radiusDynAuthServDisconBadAuthenticators)

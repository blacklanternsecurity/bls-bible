<!---------------------------------------------------------------------------------
Copyright: (c) BLS OPS LLC.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------->
# Collect and Impact
### References

### Overview
#### Impact
* Data
	* Destruction ([`Data Destruction` TTP](TTP/T1485_Data_Destruction/T1485.md))
	* Encrypted ([`Data Encrypted for Impact` TTP](TTP/T1486_Data_Encrypted_for_Impact/T1486.md))
* ([`Data Manipulation - Runtime Data Manipulation` TTP](TTP/T1565_Data_Manipulation/003_Runtime_Data_Manipulation/T1565.003.md))
* ([`Data Manipulation - Stored Data Manipulation` TTP](TTP/T1565_Data_Manipulation/001_Stored_Data_Manipulation/T1565.001.md))
* ([`Data Manipulation` TTP](TTP/T1565_Data_Manipulation/T1565.md))
* ([`Data Manipulation - Transmitted Data Manipulation` TTP](TTP/T1565_Data_Manipulation/002_Transmitted_Data_Manipulation/T1565.002.md))
* ([`Disk Wipe` TTP](TTP/T1561_Disk_Wipe/T1561.md))
* ([`Disk Wipe - Disk Content Wipe` TTP](TTP/T1561_Disk_Wipe/001_Disk_Content_Wipe/T1561.001.md))
* ([`Disk Wipe - Disk Structure Wipe` TTP](TTP/T1561_Disk_Wipe/002_Disk_Structure_Wipe/T1561.002.md))
* ([`Defacement - External Defacement` TTP](TTP/T1491_Defacement/002_External_Defacement/T1491.002.md))
* ([`Defacement - Internal Defacement` TTP](TTP/T1491_Defacement/001_Internal_Defacement/T1491.001.md))
* ([`Defacement` TTP](TTP/T1491_Defacement/T1491.md))
* ([`Firmware Corruption` TTP](TTP/T1495_Firmware_Corruption/T1495.md))
* ([`Inhibit System Recovery` TTP](TTP/T1490_Inhibit_System_Recovery/T1490.md))
* ([`Network Denial of Service - Direct Network Flood` TTP](TTP/T1498_Network_Denial_of_Service/001_Direct_Network_Flood/T1498.001.md))
* ([`Network Denial of Service - Reflection Amplification` TTP](TTP/T1498_Network_Denial_of_Service/002_Reflection_Amplification/T1498.002.md))
* ([`Network Denial of Service` TTP](TTP/T1498_Network_Denial_of_Service/T1498.md))
* ([`Resource Hijacking` TTP](TTP/T1496_Resource_Hijacking/T1496.md))
* ([`Service Stop` TTP](TTP/T1489_Service_Stop/T1489.md))
* ([`System Shutdown-Reboot` TTP](TTP/T1529_System_Shutdown-Reboot/T1529.md))
* DoS
	* Endpoints ([`Endpoint Denial of Service` TTP](TTP/T1499_Endpoint_Denial_of_Service/T1499.md))
		* OS Exhaustion Flood ([`Endpoint Denial of Service - OS Exhaustion Flood` TTP](TTP/T1499_Endpoint_Denial_of_Service/001_OS_Exhaustion_Flood/T1499.001.md))
		* Service Exhaustion Flood ([`Endpoint Denial of Service - Service Exhaustion Flood` TTP](TTP/T1499_Endpoint_Denial_of_Service/002_Service_Exhaustion_Flood/T1499.002.md))
		* Application Exhaustion Flood ([`Endpoint Denial of Service - Application Exhaustion Flood` TTP](TTP/T1499_Endpoint_Denial_of_Service/003_Application_Exhaustion_Flood/T1499.003.md))
		* App/System Exploitation ([`Endpoint Denial of Service - Application or System Exploitation` TTP](TTP/T1499_Endpoint_Denial_of_Service/004_Application_or_System_Exploitation/T1499.004.md))

#### Collect
* ([`Browser Session Hijacking` TTP](TTP/T1185_Browser_Session_Hijacking/T1185.md))
* ([`Email Collection - Email Forwarding Rule` TTP](TTP/T1114_Email_Collection/003_Email_Forwarding_Rule/T1114.003.md))
* ([`Email Collection - Local Email Collection` TTP](TTP/T1114_Email_Collection/001_Local_Email_Collection/T1114.001.md))
* ([`Email Collection - Remote Email Collection` TTP](TTP/T1114_Email_Collection/002_Remote_Email_Collection/T1114.002.md))
* ([`Email Collection` TTP](TTP/T1114_Email_Collection/T1114.md))
* ([`Archive Collected Data - Archive via Custom Method` TTP](TTP/T1560_Archive_Collected_Data/003_Archive_via_Custom_Method/T1560.003.md))
* ([`Archive Collected Data - Archive via Library` TTP](TTP/T1560_Archive_Collected_Data/002_Archive_via_Library/T1560.002.md))
* ([`Archive Collected Data - Archive via Utility` TTP](TTP/T1560_Archive_Collected_Data/001_Archive_via_Utility/T1560.001.md))
* ([`Archive Collected Data` TTP](TTP/T1560_Archive_Collected_Data/T1560.md))
* ([`Audio Capture` TTP](TTP/T1123_Audio_Capture/T1123.md))
* ([`Automated Collection Once established within a system or network` TTP](TTP/T1119_Automated_Collection_Once_established_within_a_system_or_network/T1119.md))
* ([`Clipboard Data` TTP](TTP/T1115_Clipboard_Data/T1115.md))
* ([`Data from Removable Media` TTP](TTP/T1025_Data_from_Removable_Media/T1025.md))
* ([`Data from Cloud Storage Object` TTP](TTP/T1530_Data_from_Cloud_Storage_Object/T1530.md))
* ([`Data from Configuration Repository - Network Device Configuration Dump` TTP](TTP/T1602_Data_from_Configuration_Repository/002_Network_Device_Configuration_Dump/T1602.002.md))
* ([`Data from Configuration Repository - SNMP MIB Dump` TTP](TTP/T1602_Data_from_Configuration_Repository/001_SNMP_MIB_Dump/T1602.001.md))
* ([`Data from Configuration Repository` TTP](TTP/T1602_Data_from_Configuration_Repository/T1602.md))
* ([`Data from Information Repositories - Confluence` TTP](TTP/T1213_Data_from_Information_Repositories/001_Confluence/T1213.001.md))
* ([`Data from Information Repositories - Sharepoint` TTP](TTP/T1213_Data_from_Information_Repositories/002_Sharepoint/T1213.002.md))
* ([`Data from Information Repositories` TTP](TTP/T1213_Data_from_Information_Repositories/T1213.md))
* ([`Data from Local System` TTP](TTP/T1005_Data_from_Local_System/T1005.md))
* ([`Data from Network Shared Drive` TTP](TTP/T1039_Data_from_Network_Shared_Drive/T1039.md))
* ([`Data Obfuscation` TTP](TTP/T1001_Data_Obfuscation/T1001.md))
* ([`Data Staged - Local Data Staging` TTP](TTP/T1074_Data_Staged/001_Local_Data_Staging/T1074.001.md))
* ([`Data Staged - Remote Data Staging` TTP](TTP/T1074_Data_Staged/002_Remote_Data_Staging/T1074.002.md))
* ([`Data Staged` TTP](TTP/T1074_Data_Staged/T1074.md))
* ([`Input Capture - Credential API Hooking` TTP](TTP/T1056_Input_Capture/004_Credential_API_Hooking/T1056.004.md))
* ([`Input Capture - GUI Input Capture` TTP](TTP/T1056_Input_Capture/002_GUI_Input_Capture/T1056.002.md))
* ([`Input Capture - Keylogging` TTP](TTP/T1056_Input_Capture/001_Keylogging/T1056.001.md))
* ([`Input Capture` TTP](TTP/T1056_Input_Capture/T1056.md))
* ([`Input Capture - Web Portal Capture` TTP](TTP/T1056_Input_Capture/003_Web_Portal_Capture/T1056.003.md))
* ([`Screen Capture` TTP](TTP/T1113_Screen_Capture/T1113.md))
* ([`Video Capture` TTP](TTP/T1125_Video_Capture/T1125.md))

#### Exfil
* ([`Exfiltration Over Alternative Protocol - Exfiltration Over Asymmetric Encrypted Non-C2 Protocol` TTP](TTP/T1048_Exfiltration_Over_Alternative_Protocol/002_Exfiltration_Over_Asymmetric_Encrypted_Non-C2_Protocol/T1048.002.md))
* ([`Exfiltration Over Alternative Protocol - Exfiltration Over Symmetric Encrypted Non-C2 Protocol` TTP](TTP/T1048_Exfiltration_Over_Alternative_Protocol/001_Exfiltration_Over_Symmetric_Encrypted_Non-C2_Protocol/T1048.001.md))
* ([`Exfiltration Over Alternative Protocol - Exfiltration Over Unencrypted-Obfuscated Non-C2 Protocol` TTP](TTP/T1048_Exfiltration_Over_Alternative_Protocol/003_Exfiltration_Over_Unencrypted-Obfuscated_Non-C2_Protocol/T1048.003.md))
* ([`Exfiltration Over Alternative Protocol` TTP](TTP/T1048_Exfiltration_Over_Alternative_Protocol/T1048.md))
* ([`Exfiltration Over C2 Channel` TTP](TTP/T1041_Exfiltration_Over_C2_Channel/T1041.md))
* ([`Exfiltration Over Other Network Medium - Exfiltration Over Bluetooth` TTP](TTP/T1011_Exfiltration_Over_Other_Network_Medium/001_Exfiltration_Over_Bluetooth/T1011.001.md))
* ([`Exfiltration Over Other Network Medium` TTP](TTP/T1011_Exfiltration_Over_Other_Network_Medium/T1011.md))
* ([`Exfiltration Over Physical Medium - Exfiltration over USB` TTP](TTP/T1052_Exfiltration_Over_Physical_Medium/001_Exfiltration_over_USB/T1052.001.md))
* ([`Exfiltration Over Physical Medium` TTP](TTP/T1052_Exfiltration_Over_Physical_Medium/T1052.md))
* ([`Exfiltration Over Web Service - Exfiltration to Cloud Storage` TTP](TTP/T1567_Exfiltration_Over_Web_Service/002_Exfiltration_to_Cloud_Storage/T1567.002.md))
* ([`Exfiltration Over Web Service - Exfiltration to Code Repository` TTP](TTP/T1567_Exfiltration_Over_Web_Service/001_Exfiltration_to_Code_Repository/T1567.001.md))
* ([`Exfiltration Over Web Service` TTP](TTP/T1567_Exfiltration_Over_Web_Service/T1567.md))
* ([`Scheduled Transfer` TTP](TTP/T1029_Scheduled_Transfer/T1029.md))
* ([`Transfer Data to Cloud Account` TTP](TTP/T1537_Transfer_Data_to_Cloud_Account/T1537.md))
* ([`Automated Exfiltration - Traffic Duplication` TTP](TTP/T1020_Automated_Exfiltration/001_Traffic_Duplication/T1020.001.md))
* ([`Automated Exfiltration` TTP](TTP/T1020_Automated_Exfiltration/T1020.md))
* ([`Data Transfer Size Limits` TTP](TTP/T1030_Data_Transfer_Size_Limits/T1030.md))
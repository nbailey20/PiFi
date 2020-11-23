import pyrcrack
import asyncio

### VARIABLES TO REMOVE
INTERFACE = "wlan1"


async def scanForTargets():
  air = pyrcrack.AirodumpNg()
  air.run('wlan1') 
  await asyncio.sleep(2)
  print(air.get_results())

#  async with airmon(interface) as mon:
#    async with pyrcrack.AirodumpNg() as pdump:
#      async for result in pdump(mon.monitor_interface):
#        print(result.table)
#  await asyncio.sleep(2)


asyncio.run(scanForTargets())

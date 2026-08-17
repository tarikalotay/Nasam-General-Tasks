#!/usr/bin/env python3
"""Build the full PO invoice CSV (same style as pos_sorted_by_brand.csv).

Sources:
  - PO rows exported from the vendor-PO dashboard (embedded below in RAW).
  - Delivered dates pulled from Nasam mcp_read.purchase_orders (embedded in
    DELIVERED as the UTC date of deliveredAt, matching the original file).

Commission rules (taken from the original pos_sorted_by_brand.csv):
  - Marah 6%, SONDOS 6%, Wadi Halfa 4% of received_sar, rounded half-up to 2dp.

The script validates itself against the original uploaded CSV: every row that
appears in both must match on all 14 columns.
"""

import csv
import sys
from decimal import Decimal, ROUND_HALF_UP

COMMISSION_RATE = {"Marah": Decimal("6"), "SONDOS": Decimal("6"), "Wadi Halfa": Decimal("4")}

# brand|po|channel|order_date|fc|units|requested|received|accept|fulfill|outcome
RAW = """\
Marah|13WKUXGQ|Amazon Retail|8/6/2026|JED4|8|364.8|364.8|100|100|Delivered
Marah|17WV7XMX|Amazon Retail|8/6/2026|RDF1|10|456|456|100|100|Delivered
Marah|53LUQGQJ|Amazon Retail|8/6/2026|JED4|10|110|110|100|100|Delivered
Wadi Halfa|PO2600651819|Ninja Retail|8/3/2026|JED4|140|1215.17|1215.17|100|100|Delivered
Wadi Halfa|PO2600651634|Ninja Retail|8/3/2026|RUH8|238|2008.6|2008.6|100|100|Delivered
SONDOS|1F6WGJRN|Amazon Retail|8/2/2026|RDF1|4|244.8|244.8|100|100|Delivered
Wadi Halfa|PO2600629370|Ninja Retail|7/27/2026|RUH8|116|780.95|240.91|100|31|Shortage
Wadi Halfa|PO2600629540|Ninja Retail|7/27/2026|JED4|62|396.78|68.06|100|17|Shortage
SONDOS|64TUIPCQ|Amazon Retail|7/26/2026|JED4|18|135|270|100|200|Delivered
SONDOS|2VS58KHE|Amazon Retail|7/26/2026|RDF1|2|122.4|122.4|100|100|Delivered
SONDOS|5249UCBK|Amazon Retail|7/26/2026|RUH8|2|23.5|23.5|100|100|Delivered
Marah|5249UCBK|Amazon Retail|7/26/2026|RUH8|45|247.5|247.5|100|100|Delivered
Marah|64TUIPCQ|Amazon Retail|7/26/2026|JED4|70|385|385|100|100|Delivered
Wadi Halfa|6WAWK77S|Amazon Retail|7/26/2026|RUH8|32|674.24|948.15|100|141|Delivered
Wadi Halfa|PO2600607555|Ninja Retail|7/20/2026|JED4|130|1190.02|884.78|100|74|Shortage
Wadi Halfa|PO2600607394|Ninja Retail|7/20/2026|RUH8|240|2196.96|1633.44|100|74|Shortage
Wadi Halfa|8ZI1SK8E|Amazon Retail|7/19/2026|JED4|49|446.39|0|0|0|Rejected
Wadi Halfa|5EOBBQRQ|Amazon Retail|7/19/2026|RUH8|24|218.64|0|0|0|Rejected
Marah|6Z9UWMBO|Amazon Retail|7/19/2026|RUH8|95|577.5|577.5|100|100|Delivered
SONDOS|7CS7ZUYR|Amazon Retail|7/19/2026|JED4|26|256.8|128.4|100|50|Shortage
Marah|7CS7ZUYR|Amazon Retail|7/19/2026|JED4|222|2310|2310|100|100|Delivered
SONDOS|6Z9UWMBO|Amazon Retail|7/19/2026|RUH8|6|45|45|100|100|Delivered
Marah|65T5PXVI|Amazon Retail|7/19/2026|RDF1|10|330|330|100|100|Delivered
Marah|32IYI3CV|Amazon Retail|7/14/2026|RUH8|12|547.2|0|0|0|Cancelled
Marah|6XBWLRCV|Amazon Retail|7/14/2026|JED4|6|273.6|0|0|0|Cancelled
Wadi Halfa|3KVHT2BK|Amazon Retail|7/12/2026|RUH8|22|191.2|0|0|0|Rejected
Wadi Halfa|26QOXKSP|Amazon Retail|7/12/2026|JED4|19|173.21|0|0|0|Rejected
Marah|74LAZ8YS|Amazon Retail|7/12/2026|JED4|22|495.2|385.2|100|78|Shortage
Marah|3UR2NYQH|Amazon Retail|7/12/2026|RUH8|15|82.5|82.5|100|100|Delivered
Marah|224Y4ETZ|Amazon Retail|7/12/2026|RDF1|2|206.4|206.4|100|100|Delivered
Wadi Halfa|58KW9C2W|Amazon Retail|7/8/2026|JED4|3|75|0|0|0|Cancelled
Wadi Halfa|4IRG4GZO|Amazon Retail|7/8/2026|RUH8|9|68.16|0|0|0|Cancelled
Wadi Halfa|4WXUVDTB|Amazon Retail|7/8/2026|JED4|3|13.5|0|0|0|Cancelled
Wadi Halfa|2VN7XBLN|Amazon Retail|7/7/2026|JED4|3|13.5|0|0|0|Cancelled
Wadi Halfa|87FRUE2D|Amazon Retail|7/7/2026|RUH8|2|13.61|0|0|0|Cancelled
Marah|7HEB8XWB|Amazon Retail|7/5/2026|JED4|8|408|408|100|100|Delivered
SONDOS|7X4T9L9X|Amazon Retail|7/5/2026|RUH8|8|167.4|0|100|0|Cancelled
Marah|7X4T9L9X|Amazon Retail|7/5/2026|RUH8|81|458.72|440|100|96|Shortage
Marah|6HIM13WU|Amazon Retail|7/5/2026|RDF1|2|73.2|73.2|100|100|Delivered
Wadi Halfa|7WSXCEOX|Amazon Retail|7/5/2026|RUH8|2|18.22|0|0|0|Cancelled
Wadi Halfa|78WHY2TK|Amazon Retail|7/5/2026|JED4|11|100.33|0|0|0|Cancelled
Wadi Halfa|6YZAV7QM|Amazon Retail|7/2/2026|RUH8|17|154.87|0|100|0|Unfulfilled
Wadi Halfa|2J8AQOKT|Amazon Retail|7/2/2026|JED4|37|337.07|0|0|0|Cancelled
Wadi Halfa|5P6LCJKX|Amazon Retail|6/28/2026|JED4|3|27.45|0|0|0|Cancelled
Wadi Halfa|4KDCOEYS|Amazon Retail|6/28/2026|RUH8|32|650.32|632.1|100|97|Shortage
Marah|2AMQJ9LR|Amazon Retail|6/28/2026|RUH8|5|27.5|27.5|100|100|Delivered
SONDOS|2AMQJ9LR|Amazon Retail|6/28/2026|RUH8|2|122.4|122.4|100|100|Delivered
Wadi Halfa|523FHETX|Amazon Retail|6/22/2026|RUH8|61|786.25|321.75|100|41|Shortage
Wadi Halfa|556EF2MV|Amazon Retail|6/22/2026|JED4|5|31.72|0|0|0|Cancelled
Marah|5R5X8LID|Amazon Retail|6/21/2026|JED4|9|201.4|201.4|100|100|Delivered
Marah|6DPTSK1M|Amazon Retail|6/21/2026|RUH8|13|157.9|157.9|100|100|Delivered
SONDOS|6DPTSK1M|Amazon Retail|6/21/2026|RUH8|4|244.8|244.8|100|100|Delivered
SONDOS|34RW3MWX|Amazon Retail|6/21/2026|RDF1|2|76.8|76.8|100|100|Delivered
Marah|6YXQJTKI|Amazon Retail|6/14/2026|RUH8|137|833.7|833.7|100|100|Delivered
SONDOS|8MHCMNQO|Amazon Retail|6/14/2026|JED4|32|991.8|991.8|100|100|Delivered
Marah|8MHCMNQO|Amazon Retail|6/14/2026|JED4|20|660|660|100|100|Delivered
SONDOS|6YXQJTKI|Amazon Retail|6/14/2026|RUH8|8|167.4|212.4|100|127|Delivered
SONDOS|78GBUJ1W|Amazon Retail|6/14/2026|RDF1|1|102.8|102.8|100|100|Delivered
Marah|78GBUJ1W|Amazon Retail|6/14/2026|RDF1|12|367.2|367.2|100|100|Delivered
Marah|27HTOR4Q|Amazon Retail|6/7/2026|RUH8|2|91.2|91.2|100|100|Delivered
SONDOS|77DN671B|Amazon Retail|6/7/2026|JED4|2|122.4|0|100|0|Cancelled
Marah|77DN671B|Amazon Retail|6/7/2026|JED4|10|348|91.2|100|26|Cancelled
Marah|25WE4Y7O|Amazon Retail|5/31/2026|JED4|2|55.2|0|100|0|Cancelled
Marah|31WXVSCY|Amazon Retail|5/31/2026|RUH8|2|73.2|73.2|100|100|Delivered
Marah|2B23XHGH|Amazon Retail|5/24/2026|JED4|32|716.7|700.3|100|98|Shortage
SONDOS|2B23XHGH|Amazon Retail|5/24/2026|JED4|6|367.2|367.2|100|100|Delivered
SONDOS|57VZIBCA|Amazon Retail|5/24/2026|RUH8|10|612|612|100|100|Delivered
Marah|57VZIBCA|Amazon Retail|5/24/2026|RUH8|9|530.4|242.4|100|46|Shortage
Marah|4J9CPFNV|Amazon Retail|5/17/2026|RUH8|3|102.9|102.9|100|100|Delivered
SONDOS|4J9CPFNV|Amazon Retail|5/17/2026|RUH8|2|122.4|122.4|100|100|Delivered
Marah|6G32T7VG|Amazon Retail|5/17/2026|JED4|2|206.4|206.4|100|100|Delivered
Marah|5YTDVHBW|Amazon Retail|5/14/2026|RUH8|235|1292.5|1287|100|100|Shortage
Marah|64ZRO2IW|Amazon Retail|5/14/2026|JED4|280|1540|1540|100|100|Delivered
Marah|4HJZN3HS|Amazon Retail|5/14/2026|JED4|5|168.9|65.1|100|39|Shortage
SONDOS|4VVUV3LF|Amazon Retail|5/14/2026|RUH8|2|57.6|0|100|0|Unfulfilled
Marah|6YXMCSBG|Amazon Retail|5/10/2026|RUH8|4|182.4|182.4|100|100|Delivered
SONDOS|6YXMCSBG|Amazon Retail|5/10/2026|RUH8|4|244.8|244.8|100|100|Delivered
Marah|7FQQP3YA|Amazon Retail|5/10/2026|JED4|9|364.8|364.8|100|100|Delivered
SONDOS|87KN8WEU|Amazon Retail|5/10/2026|RDF1|2|124.8|0|100|0|Cancelled
Marah|5ZC4GIJB|Amazon Retail|5/3/2026|JED4|6|278.4|758.4|100|272|Delivered
Marah|4DM5ZX9S|Amazon Retail|5/3/2026|RUH8|6|278.4|758.4|100|272|Delivered
SONDOS|4DM5ZX9S|Amazon Retail|5/3/2026|RUH8|16|979.2|979.2|100|100|Delivered
Marah|5C8HGLYP|Amazon Retail|4/26/2026|JED4|12|146.2|237.4|100|162|Delivered
SONDOS|2ZQ63SQZ|Amazon Retail|4/26/2026|RUH8|4|244.8|244.8|100|100|Delivered
Marah|2ZQ63SQZ|Amazon Retail|4/26/2026|RUH8|17|173.7|173.7|100|100|Delivered
SONDOS|5C8HGLYP|Amazon Retail|4/26/2026|JED4|10|612|734.4|100|120|Delivered
Marah|5A5RRTQI|Amazon Retail|4/19/2026|JED4|250|1579.82|1552.32|100|98|Shortage
Marah|45NJYTSJ|Amazon Retail|4/19/2026|RUH8|70|594.5|382.7|100|64|Shortage
Marah|2FMA3P2X|Amazon Retail|4/12/2026|RUH8|245|1485|1540|100|104|Delivered
SONDOS|2FMA3P2X|Amazon Retail|4/12/2026|RUH8|6|367.2|489.6|100|133|Delivered
SONDOS|5PE3P2GE|Amazon Retail|4/12/2026|JED4|15|959.6|959.6|100|100|Delivered
Marah|5PE3P2GE|Amazon Retail|4/12/2026|JED4|325|2439.4|2605|100|107|Delivered
Marah|8GDABTDG|Amazon Retail|4/5/2026|JED4|311|1833.72|1833.72|100|100|Delivered
Marah|2I94WCYC|Amazon Retail|4/5/2026|RUH8|185|1045|990|100|95|Shortage
Marah|12NKR58W|Amazon Retail|3/29/2026|JED4|5|55|110|100|200|Delivered
SONDOS|6NWUZ15U|Amazon Retail|3/29/2026|RUH8|10|612|612|100|100|Delivered
Marah|7WF53VUB|Amazon Retail|3/29/2026|JED4|90|495|495|100|100|Delivered
Marah|6NWUZ15U|Amazon Retail|3/29/2026|RUH8|6|219.6|183|100|83|Shortage
SONDOS|1Y1T5K2Z|Amazon Retail|3/22/2026|JED4|10|612|612|100|100|Delivered
SONDOS|1KBAMBMY|Amazon Retail|3/22/2026|RUH8|12|412.2|412.2|100|100|Delivered
Marah|1KBAMBMY|Amazon Retail|3/22/2026|RUH8|2|23.4|23.4|100|100|Delivered
SONDOS|3EO1QUXF|Amazon Retail|3/15/2026|JED4|1|102.8|102.8|100|100|Delivered
Marah|7BB3BSGS|Amazon Retail|3/15/2026|RUH8|6|273.6|364.8|100|133|Delivered
Marah|6BQUXPAB|Amazon Retail|3/8/2026|JED4|4|182.4|182.4|100|100|Delivered
SONDOS|56ODNFEU|Amazon Retail|3/8/2026|RUH8|2|122.4|122.4|100|100|Delivered
Marah|56ODNFEU|Amazon Retail|3/8/2026|RUH8|4|181.2|181.2|100|100|Delivered
Marah|33272MDV|Amazon Retail|3/1/2026|RUH8|14|219.44|72|100|33|Shortage
SONDOS|33272MDV|Amazon Retail|3/1/2026|RUH8|4|244.8|244.8|100|100|Delivered
Marah|4VGJUUTB|Amazon Retail|3/1/2026|JED4|1|36|36|100|100|Delivered
SONDOS|4VGJUUTB|Amazon Retail|3/1/2026|JED4|4|244.8|244.8|100|100|Delivered
Marah|8MME3VWE|Amazon Retail|2/26/2026|JED4|2|91.2|91.2|100|100|Delivered
SONDOS|85YJNW7Z|Amazon Retail|2/26/2026|RUH8|10|612|612|100|100|Delivered
SONDOS|8MME3VWE|Amazon Retail|2/26/2026|JED4|6|367.2|367.2|100|100|Delivered
Marah|47SZZRUF|Amazon Retail|2/22/2026|JED4|134|891.62|794.92|100|89|Shortage
Marah|5CHSK8EF|Amazon Retail|2/22/2026|RUH8|6|219.6|219.6|100|100|Delivered
SONDOS|47SZZRUF|Amazon Retail|2/22/2026|JED4|2|122.4|61.2|100|50|Shortage
Marah|1NS5YK4C|Amazon Retail|2/15/2026|JED4|1|18.72|0|100|0|Cancelled
Marah|2Q2CPLWE|Amazon Retail|2/13/2026|JED4|5|55|55|100|100|Delivered
Marah|2NMPDC6A|Amazon Retail|2/8/2026|JED4|101|1366.02|1120.82|100|82|Delivered
SONDOS|2NMPDC6A|Amazon Retail|2/8/2026|JED4|40|1465.8|135|100|9|Shortage
Marah|63CNSAWW|Amazon Retail|2/8/2026|RUH8|14|386.4|386.4|100|100|Delivered
SONDOS|2776KBES|Amazon Retail|2/1/2026|JED4|8|390.7|390.7|100|100|Delivered
Marah|2776KBES|Amazon Retail|2/1/2026|JED4|7|218.4|218.4|100|100|Delivered
Marah|35A5IQ5O|Amazon Retail|2/1/2026|RUH8|2|55.2|55.2|100|100|Delivered
SONDOS|4Q9D66FC|Amazon Retail|1/29/2026|JED4|10|117.5|117.5|100|100|Delivered
Marah|3NBXS26G|Amazon Retail|1/25/2026|JED4|5|55|55|100|100|Delivered
Marah|2B5T42JL|Amazon Retail|1/14/2026|JED4|70|385|379.5|100|99|Shortage
Marah|4MD92H1G|Amazon Retail|1/14/2026|RUH8|180|990|990|100|100|Delivered
Marah|6S9RVIGN|Amazon Retail|1/11/2026|JED4|189|1312.5|1209.6|100|92|Shortage
Marah|8GLJBAPU|Amazon Retail|1/11/2026|RUH8|337|1915.7|1888.2|100|99|Shortage
SONDOS|6S9RVIGN|Amazon Retail|1/11/2026|JED4|2|76.8|76.8|100|100|Delivered
SONDOS|1G7W4QOA|Amazon Retail|1/4/2026|RUH8|4|201.6|124.8|100|62|Shortage
Marah|6PH6KTZF|Amazon Retail|1/4/2026|JED4|2|73.2|73.2|100|100|Delivered
SONDOS|6PH6KTZF|Amazon Retail|1/4/2026|JED4|1|102.8|102.8|100|100|Delivered
SONDOS|5ILLL7BX|Amazon Retail|12/31/2025|JED4|2|63.6|254.4|100|400|Delivered
SONDOS|6UBMEEFU|Amazon Retail|12/28/2025|JED4|1|11.75|70.5|100|600|Delivered
Marah|6V3M52MA|Amazon Retail|12/28/2025|RUH8|6|219.6|219.6|100|100|Delivered
Marah|6UBMEEFU|Amazon Retail|12/28/2025|JED4|2|73.2|73.2|100|100|Delivered
SONDOS|6V3M52MA|Amazon Retail|12/28/2025|RUH8|2|122.4|122.4|100|100|Delivered
Marah|6PSDP49U|Amazon Retail|12/21/2025|JED4|12|349.2|349.2|100|100|Delivered
SONDOS|6PSDP49U|Amazon Retail|12/21/2025|JED4|2|106.8|0|100|0|Cancelled
Marah|797EACNS|Amazon Retail|12/21/2025|RUH8|14|609.6|609.6|100|100|Delivered
Marah|6TDL7ZQP|Amazon Retail|12/14/2025|RUH8|29|283.9|333.5|100|117|Delivered
SONDOS|7M6TKRHR|Amazon Retail|12/7/2025|RUH8|2|26.66|26.66|100|100|Delivered
Marah|7M6TKRHR|Amazon Retail|12/7/2025|RUH8|30|192.5|143|100|74|Shortage
Marah|6CZVU75G|Amazon Retail|12/7/2025|JED4|8|339.84|136.8|100|40|Shortage
Marah|5EN36W7Q|Amazon Retail|12/7/2025|XKSR|8|220.8|220.8|100|100|Delivered
SONDOS|6CZVU75G|Amazon Retail|12/7/2025|JED4|8|202.38|239.94|100|119|Delivered
Marah|2P93YCEF|Amazon Retail|11/30/2025|XKSR|4|110.4|110.4|100|100|Delivered
SONDOS|6DY1IPME|Amazon Retail|11/30/2025|RUH8|93|1808.25|1898.25|100|105|Delivered
Marah|6WB73PWY|Amazon Retail|11/30/2025|JED4|235|1496.5|2003|100|134|Delivered
Marah|6DY1IPME|Amazon Retail|11/30/2025|RUH8|5|199.2|244.8|100|123|Delivered
SONDOS|6WB73PWY|Amazon Retail|11/30/2025|JED4|89|2358.45|2511.45|100|106|Delivered
Marah|1JV74U5F|Amazon Retail|11/23/2025|JED4|803|5076.8|0|0|0|Cancelled
SONDOS|2ZICET5J|Amazon Retail|11/23/2025|RUH8|110|2179.3|0|0|0|Cancelled
Marah|4PTXU81M|Amazon Retail|11/23/2025|XKSR|2|96|0|0|0|Cancelled
SONDOS|1JV74U5F|Amazon Retail|11/23/2025|JED4|112|3112.85|0|0|0|Cancelled
Marah|2ZICET5J|Amazon Retail|11/23/2025|RUH8|22|455.4|0|0|0|Cancelled
Marah|3VQF583P|Amazon Retail|11/16/2025|JED4|19|474.8|0|0|0|Cancelled
SONDOS|3VQF583P|Amazon Retail|11/16/2025|JED4|96|2974.85|0|0|0|Cancelled
SONDOS|7J5A33FT|Amazon Retail|11/16/2025|RUH8|103|2444.75|0|0|0|Cancelled
Marah|7J5A33FT|Amazon Retail|11/16/2025|RUH8|17|524.2|0|0|0|Cancelled
Marah|6V2QLC8V|Amazon Retail|11/10/2025|RUH8|1|36|0|0|0|Cancelled
Marah|3VGCXDFL|Amazon Retail|11/10/2025|JED4|3|108|0|0|0|Cancelled
Marah|4SOV5ZPQ|Amazon Retail|11/9/2025|RUH8|566|3143.5|0|0|0|Cancelled
Marah|89E9VAQM|Amazon Retail|11/9/2025|JED4|573|3586.4|0|0|0|Cancelled
SONDOS|4SOV5ZPQ|Amazon Retail|11/9/2025|RUH8|80|1476.2|0|0|0|Cancelled
SONDOS|89E9VAQM|Amazon Retail|11/9/2025|JED4|62|2288.6|0|0|0|Cancelled
Marah|4ELTCYLQ|Amazon Retail|11/6/2025|JED4|2|72|0|0|0|Cancelled
Marah|2PRVZ2QJ|Amazon Retail|11/6/2025|RUH8|2|72|0|0|0|Cancelled
SONDOS|4MXAY6IE|Amazon Retail|11/6/2025|JED4|1|102.8|0|0|0|Cancelled
Marah|7CR8MEDE|Amazon Retail|11/2/2025|JED4|513|3240.2|0|0|0|Cancelled
SONDOS|7CR8MEDE|Amazon Retail|11/2/2025|JED4|26|1150.9|0|0|0|Cancelled
SONDOS|481D75AL|Amazon Retail|11/2/2025|RUH8|31|881.15|0|0|0|Cancelled
Marah|481D75AL|Amazon Retail|11/2/2025|RUH8|407|2281.9|0|0|0|Cancelled
SONDOS|8RSMCYZA|Amazon Retail|10/26/2025|RUH8|30|225|0|0|0|Cancelled
SONDOS|7PSVFJOX|Amazon Retail|10/26/2025|JED4|30|1548.78|0|0|0|Cancelled
Marah|8RSMCYZA|Amazon Retail|10/26/2025|RUH8|281|1582.7|0|0|0|Cancelled
Marah|7PSVFJOX|Amazon Retail|10/26/2025|JED4|123|892.7|0|0|0|Cancelled
Marah|71RVXBLU|Amazon Retail|10/21/2025|RUH8|2|51.6|0|0|0|Cancelled
SONDOS|78NAQWEM|Amazon Retail|10/19/2025|RUH8|14|212.4|0|0|0|Cancelled
Marah|78NAQWEM|Amazon Retail|10/19/2025|RUH8|320|1911.5|0|0|0|Cancelled
SONDOS|5NRV1UJB|Amazon Retail|10/19/2025|JED4|20|1224|0|0|0|Cancelled
Marah|5NRV1UJB|Amazon Retail|10/19/2025|JED4|128|898.1|0|0|0|Cancelled
Marah|4TN3ZVSL|Amazon Retail|10/12/2025|JED4|21|609.4|288|100|47|Cancelled
SONDOS|4TN3ZVSL|Amazon Retail|10/12/2025|JED4|8|476.4|0|100|0|Cancelled
SONDOS|6PP725QB|Amazon Retail|10/12/2025|RUH8|18|1101.6|1101.6|100|100|Delivered
Marah|6PP725QB|Amazon Retail|10/12/2025|RUH8|20|223.5|110|100|49|Shortage
Marah|13XNC3UZ|Amazon Retail|10/5/2025|JED4|36|1279.2|0|0|0|Cancelled
SONDOS|13XNC3UZ|Amazon Retail|10/5/2025|JED4|4|164.4|0|0|0|Cancelled
SONDOS|8C8ZHJUB|Amazon Retail|10/5/2025|RUH8|12|90|0|0|0|Cancelled
Marah|8C8ZHJUB|Amazon Retail|10/5/2025|RUH8|5|55|0|0|0|Cancelled
SONDOS|32EZOEJU|Amazon Retail|9/28/2025|RUH8|1|102.8|205.6|100|200|Delivered
SONDOS|2OR6EQMN|Amazon Retail|9/28/2025|JED4|6|331.64|0|100|0|Cancelled
Marah|2OR6EQMN|Amazon Retail|9/28/2025|JED4|5|55|0|100|0|Cancelled
Marah|3EZ3B41A|Amazon Retail|9/25/2025|JED4|5|55|0|100|0|Cancelled
SONDOS|6CRLP61F|Amazon Retail|9/21/2025|JED4|5|309.2|0|100|0|Cancelled
SONDOS|8VVFT9PI|Amazon Retail|9/14/2025|JED4|6|328.8|0|0|0|Cancelled
Marah|8VVFT9PI|Amazon Retail|9/14/2025|JED4|76|2138.4|0|0|0|Cancelled
"""

# brand|po|delivered date (UTC date of deliveredAt from Nasam purchase_orders)
DELIVERED = """\
Marah|8VVFT9PI|2026-03-01
Marah|3EZ3B41A|2026-03-01
Marah|2OR6EQMN|2026-03-01
Marah|8C8ZHJUB|2026-03-01
Marah|13XNC3UZ|2026-03-01
Marah|6PP725QB|2025-11-02
Marah|4TN3ZVSL|2025-12-31
Marah|5NRV1UJB|2026-03-01
Marah|78NAQWEM|2026-03-01
Marah|71RVXBLU|2026-03-01
Marah|7PSVFJOX|2026-03-01
Marah|8RSMCYZA|2026-03-01
Marah|481D75AL|2026-03-01
Marah|7CR8MEDE|2026-03-01
Marah|2PRVZ2QJ|2026-03-01
Marah|4ELTCYLQ|2026-03-01
Marah|4SOV5ZPQ|2026-03-01
Marah|89E9VAQM|2026-03-01
Marah|3VGCXDFL|2026-03-01
Marah|6V2QLC8V|2026-03-01
Marah|3VQF583P|2026-03-01
Marah|7J5A33FT|2026-03-01
Marah|1JV74U5F|2026-03-01
Marah|2ZICET5J|2026-03-01
Marah|4PTXU81M|2026-03-01
Marah|2P93YCEF|2025-12-17
Marah|6DY1IPME|2026-01-08
Marah|6WB73PWY|2026-02-28
Marah|5EN36W7Q|2025-12-17
Marah|6CZVU75G|2025-12-31
Marah|7M6TKRHR|2026-01-02
Marah|6TDL7ZQP|2025-12-27
Marah|797EACNS|2025-12-27
Marah|6PSDP49U|2025-12-27
Marah|6UBMEEFU|2026-01-04
Marah|6V3M52MA|2026-01-04
Marah|6PH6KTZF|2026-01-08
Marah|6S9RVIGN|2026-01-19
Marah|8GLJBAPU|2026-01-24
Marah|2B5T42JL|2026-03-01
Marah|4MD92H1G|2026-01-24
Marah|3NBXS26G|2026-02-03
Marah|2776KBES|2026-02-05
Marah|35A5IQ5O|2026-02-04
Marah|2NMPDC6A|2026-03-03
Marah|63CNSAWW|2026-02-12
Marah|2Q2CPLWE|2026-02-20
Marah|1NS5YK4C|2026-03-22
Marah|47SZZRUF|2026-03-06
Marah|5CHSK8EF|2026-03-06
Marah|8MME3VWE|2026-03-22
Marah|33272MDV|2026-03-29
Marah|4VGJUUTB|2026-03-22
Marah|56ODNFEU|2026-03-12
Marah|6BQUXPAB|2026-03-12
Marah|7BB3BSGS|2026-08-11
Marah|1KBAMBMY|2026-04-03
Marah|6NWUZ15U|2026-05-06
Marah|7WF53VUB|2026-08-11
Marah|12NKR58W|2026-06-06
Marah|2I94WCYC|2026-04-28
Marah|8GDABTDG|2026-04-18
Marah|2FMA3P2X|2026-04-28
Marah|5PE3P2GE|2026-04-20
Marah|45NJYTSJ|2026-06-08
Marah|5A5RRTQI|2026-04-23
Marah|2ZQ63SQZ|2026-05-01
Marah|5C8HGLYP|2026-06-09
Marah|4DM5ZX9S|2026-05-08
Marah|5ZC4GIJB|2026-05-07
Marah|6YXMCSBG|2026-05-20
Marah|7FQQP3YA|2026-05-14
Marah|4HJZN3HS|2026-05-20
Marah|5YTDVHBW|2026-05-23
Marah|64ZRO2IW|2026-05-19
Marah|6G32T7VG|2026-06-07
Marah|4J9CPFNV|2026-06-11
Marah|2B23XHGH|2026-06-18
Marah|57VZIBCA|2026-06-03
Marah|25WE4Y7O|2026-07-29
Marah|31WXVSCY|2026-06-07
Marah|27HTOR4Q|2026-06-10
Marah|77DN671B|2026-07-14
Marah|6YXQJTKI|2026-06-18
Marah|78GBUJ1W|2026-06-20
Marah|8MHCMNQO|2026-06-17
Marah|5R5X8LID|2026-06-28
Marah|6DPTSK1M|2026-06-24
Marah|2AMQJ9LR|2026-07-01
Marah|6HIM13WU|2026-07-08
Marah|7X4T9L9X|2026-07-10
Marah|7HEB8XWB|2026-07-08
Marah|224Y4ETZ|2026-07-15
Marah|3UR2NYQH|2026-07-14
Marah|74LAZ8YS|2026-07-14
Marah|32IYI3CV|2026-07-29
Marah|6XBWLRCV|2026-07-29
Marah|65T5PXVI|2026-07-28
Marah|6Z9UWMBO|2026-07-29
Marah|7CS7ZUYR|2026-07-29
Marah|5249UCBK|2026-07-28
Marah|64TUIPCQ|2026-08-09
Marah|53LUQGQJ|2026-08-12
Marah|13WKUXGQ|2026-08-12
Marah|17WV7XMX|2026-08-11
SONDOS|8VVFT9PI|2026-03-01
SONDOS|6CRLP61F|2026-03-01
SONDOS|2OR6EQMN|2026-03-01
SONDOS|32EZOEJU|2026-03-01
SONDOS|8C8ZHJUB|2026-03-01
SONDOS|13XNC3UZ|2026-03-01
SONDOS|6PP725QB|2025-11-02
SONDOS|4TN3ZVSL|2025-12-31
SONDOS|5NRV1UJB|2026-03-01
SONDOS|78NAQWEM|2026-03-01
SONDOS|7PSVFJOX|2026-03-01
SONDOS|8RSMCYZA|2026-03-01
SONDOS|481D75AL|2026-03-01
SONDOS|7CR8MEDE|2026-03-01
SONDOS|4MXAY6IE|2026-03-01
SONDOS|4SOV5ZPQ|2026-03-01
SONDOS|89E9VAQM|2026-03-01
SONDOS|3VQF583P|2026-03-01
SONDOS|7J5A33FT|2026-03-01
SONDOS|1JV74U5F|2026-03-01
SONDOS|2ZICET5J|2026-03-01
SONDOS|6DY1IPME|2026-01-08
SONDOS|6WB73PWY|2026-02-28
SONDOS|6CZVU75G|2025-12-31
SONDOS|7M6TKRHR|2026-01-02
SONDOS|6PSDP49U|2025-12-27
SONDOS|6UBMEEFU|2026-01-04
SONDOS|6V3M52MA|2026-01-04
SONDOS|5ILLL7BX|2026-01-04
SONDOS|1G7W4QOA|2026-01-08
SONDOS|6PH6KTZF|2026-01-08
SONDOS|6S9RVIGN|2026-01-19
SONDOS|4Q9D66FC|2026-02-04
SONDOS|2776KBES|2026-02-05
SONDOS|2NMPDC6A|2026-03-03
SONDOS|47SZZRUF|2026-03-06
SONDOS|85YJNW7Z|2026-03-29
SONDOS|8MME3VWE|2026-03-22
SONDOS|33272MDV|2026-03-29
SONDOS|4VGJUUTB|2026-03-22
SONDOS|56ODNFEU|2026-03-12
SONDOS|3EO1QUXF|2026-03-30
SONDOS|1KBAMBMY|2026-04-03
SONDOS|1Y1T5K2Z|2026-04-06
SONDOS|6NWUZ15U|2026-05-06
SONDOS|2FMA3P2X|2026-04-28
SONDOS|5PE3P2GE|2026-04-20
SONDOS|2ZQ63SQZ|2026-05-01
SONDOS|5C8HGLYP|2026-06-09
SONDOS|4DM5ZX9S|2026-05-08
SONDOS|6YXMCSBG|2026-05-20
SONDOS|87KN8WEU|2026-08-11
SONDOS|4VVUV3LF|2026-06-01
SONDOS|4J9CPFNV|2026-06-11
SONDOS|2B23XHGH|2026-06-18
SONDOS|57VZIBCA|2026-06-03
SONDOS|77DN671B|2026-07-14
SONDOS|6YXQJTKI|2026-06-18
SONDOS|78GBUJ1W|2026-06-20
SONDOS|8MHCMNQO|2026-06-17
SONDOS|34RW3MWX|2026-06-24
SONDOS|6DPTSK1M|2026-06-24
SONDOS|2AMQJ9LR|2026-07-01
SONDOS|7X4T9L9X|2026-07-10
SONDOS|6Z9UWMBO|2026-07-29
SONDOS|7CS7ZUYR|2026-07-29
SONDOS|2VS58KHE|2026-07-28
SONDOS|5249UCBK|2026-07-28
SONDOS|64TUIPCQ|2026-08-09
SONDOS|1F6WGJRN|2026-08-04
Wadi Halfa|523FHETX|2026-07-10
Wadi Halfa|556EF2MV|2026-07-01
Wadi Halfa|4KDCOEYS|2026-07-10
Wadi Halfa|5P6LCJKX|2026-07-05
Wadi Halfa|2J8AQOKT|2026-07-29
Wadi Halfa|6YZAV7QM|2026-07-29
Wadi Halfa|78WHY2TK|2026-07-12
Wadi Halfa|7WSXCEOX|2026-07-12
Wadi Halfa|2VN7XBLN|2026-07-29
Wadi Halfa|87FRUE2D|2026-07-29
Wadi Halfa|4IRG4GZO|2026-07-29
Wadi Halfa|4WXUVDTB|2026-07-29
Wadi Halfa|58KW9C2W|2026-07-29
Wadi Halfa|26QOXKSP|2026-07-19
Wadi Halfa|3KVHT2BK|2026-07-19
Wadi Halfa|5EOBBQRQ|2026-07-26
Wadi Halfa|8ZI1SK8E|2026-07-26
Wadi Halfa|PO2600607394|2026-08-13
Wadi Halfa|PO2600607555|2026-08-13
Wadi Halfa|6WAWK77S|2026-08-11
Wadi Halfa|PO2600629370|2026-08-13
Wadi Halfa|PO2600629540|2026-08-13
Wadi Halfa|PO2600651634|2026-08-13
Wadi Halfa|PO2600651819|2026-08-13
"""

HEADER = [
    "brand", "po_number", "channel", "order_date", "delivered_date",
    "fulfillment_center", "units", "requested_sar", "received_sar",
    "accept_pct", "fulfill_pct", "outcome", "commission_rate_pct", "commission_sar",
]


def fmt(d: Decimal) -> str:
    """Trailing-zero-free number formatting matching the original CSV (364.8, 110, 68.06)."""
    return format(d.normalize(), "f")


def mdy(iso: str) -> str:
    """2026-08-12 -> 8/12/2026 (no leading zeros, matching the original CSV)."""
    y, m, d = iso.split("-")
    return f"{int(m)}/{int(d)}/{y}"


def date_key(mdy_str: str):
    m, d, y = mdy_str.split("/")
    return (int(y), int(m), int(d))


def main() -> int:
    delivered = {}
    for line in DELIVERED.strip().splitlines():
        brand, po, iso = line.split("|")
        delivered[(brand, po)] = mdy(iso)

    rows = []
    for line in RAW.strip().splitlines():
        brand, po, channel, odate, fc, units, req, rec, acc, ful, outcome = line.split("|")
        rate = COMMISSION_RATE[brand]
        commission = (Decimal(rec) * rate / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        rows.append([
            brand, po, channel, odate, delivered[(brand, po)], fc, units,
            fmt(Decimal(req)), fmt(Decimal(rec)), acc, ful, outcome,
            fmt(rate), fmt(commission),
        ])

    # --- validations -------------------------------------------------------
    assert len(rows) == 199, f"expected 199 rows, got {len(rows)}"
    keys = {(r[0], r[1]) for r in rows}
    assert len(keys) == len(rows), "duplicate (brand, po) row"
    unused = set(delivered) - keys
    assert not unused, f"delivered-map entries with no PO row: {sorted(unused)}"

    # Every row that also exists in the original uploaded CSV must match exactly.
    original = sys.argv[1] if len(sys.argv) > 1 else None
    checked = 0
    if original:
        with open(original, newline="") as f:
            for orig in csv.reader(f):
                if not orig or orig[0] == "brand":
                    continue
                mine = next(r for r in rows if (r[0], r[1]) == (orig[0], orig[1]))
                assert mine == orig, f"mismatch vs original for {orig[0]}/{orig[1]}:\n  orig: {orig}\n  mine: {mine}"
                checked += 1
        assert checked == 23, f"expected 23 overlap rows, checked {checked}"

    # --- output ------------------------------------------------------------
    rows.sort(key=lambda r: (r[0], date_key(r[3]), r[1]))
    out = "pos_invoices_sorted_by_brand.csv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)

    print(f"OK: wrote {out} with {len(rows)} rows (validated {checked} against original)")
    for brand in ("Marah", "SONDOS", "Wadi Halfa"):
        b = [r for r in rows if r[0] == brand]
        units = sum(int(r[6]) for r in b)
        req = sum(Decimal(r[7]) for r in b)
        rec = sum(Decimal(r[8]) for r in b)
        com = sum(Decimal(r[13]) for r in b)
        print(f"{brand}: {len(b)} rows, {units} units, requested {req}, received {rec}, commission {com}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Closed retail POs pulled DIRECTLY from mcp_read.purchase_orders — 4 Oct 2026.
# Q2 is closed: the view now exposes requestedValue / acceptedValue / receivedValue alongside the
# three stages and an `outcome` label, so the closed-PO CSV export is retired. Retail commission is
# charged on RECEIVED value, so receivedValue is the base.
#
# Refresh each run:
#   SELECT brandName, channelName, month(COALESCE(deliveredAt, orderDate)), SUM(receivedValue)
#   FROM mcp_read.purchase_orders WHERE status='Closed' AND COALESCE(deliveredAt,orderDate) >= '2025-11-01'
# Every closed outcome counts (successfulDelivery, deliveredWithShortage, cancelled, rejected,
# unfulfilled): a cancelled or short PO can still have received units, and those are billable.
# Check two things each run — receivedValue IS NULL (a stage nobody recorded, never treated as 0)
# and acceptedUnits IS NULL (which would make a `rejected`/`unfulfilled` outcome untrustworthy).
# Both were zero across all 27 brand-channel-months in this pull.
# (brand, channel, ym, received_sar)
PO_CLOSED=[
("Marah","Amazon Retail","2025-11",110.00),
("Marah","Amazon Retail","2025-12",2048.30),
("Marah","Amazon Retail","2026-01",4841.60),
("Marah","Amazon Retail","2026-02",2773.00),
("Marah","Amazon Retail","2026-03",3077.64),
("Marah","Amazon Retail","2026-04",8544.44),
("Marah","Amazon Retail","2026-05",5312.80),
("Marah","Amazon Retail","2026-06",4366.70),
("Marah","Amazon Retail","2026-07",5179.00),
("Marah","Amazon Retail","2026-08",6513.40),
("Marah","Amazon Retail","2026-09",4132.90),
("SONDOS","Amazon Retail","2025-11",1101.60),
("SONDOS","Amazon Retail","2025-12",239.94),
("SONDOS","Amazon Retail","2026-01",2676.61),
("SONDOS","Amazon Retail","2026-02",3019.65),
("SONDOS","Amazon Retail","2026-03",2095.80),
("SONDOS","Amazon Retail","2026-04",2473.40),
("SONDOS","Amazon Retail","2026-05",2080.80),
("SONDOS","Amazon Retail","2026-06",3464.60),
("SONDOS","Amazon Retail","2026-07",441.70),
("SONDOS","Amazon Retail","2026-08",1801.20),
("SONDOS","Amazon Retail","2026-09",2120.40),
("Wadi Halfa","Amazon Retail","2026-07",953.85),
("Wadi Halfa","Amazon Retail","2026-08",3266.32),
("Wadi Halfa","Amazon Retail","2026-09",6043.44),
("Wadi Halfa","Ninja Retail","2026-08",9120.70),
("Wadi Halfa","Ninja Retail","2026-09",13231.84),
]
# commission rate per brand on retail
RETAIL_RATE={"Marah":0.06,"SONDOS":0.06,"Wadi Halfa":0.04}

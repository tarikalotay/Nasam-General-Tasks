# Closed retail POs pulled DIRECTLY from mcp_read.purchase_orders (values shipped 20 Aug 2026).
# Refresh each run: SELECT brand, channel, month(deliveredAt||orderDate), SUM(receivedValue)
#   WHERE outcome IN (successfulDelivery, deliveredWithShortage, cancelled, rejected, unfulfilled)
# Pulled 23 Aug 2026. (brand, channel, ym, received_sar)
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
("Marah","Amazon Retail","2026-08",2753.10),
("SONDOS","Amazon Retail","2025-11",1101.60),
("SONDOS","Amazon Retail","2025-12",239.94),
("SONDOS","Amazon Retail","2026-01",2676.61),
("SONDOS","Amazon Retail","2026-02",3019.65),
("SONDOS","Amazon Retail","2026-03",2095.80),
("SONDOS","Amazon Retail","2026-04",2473.40),
("SONDOS","Amazon Retail","2026-05",2080.80),
("SONDOS","Amazon Retail","2026-06",3464.60),
("SONDOS","Amazon Retail","2026-07",441.70),
("SONDOS","Amazon Retail","2026-08",759.60),
("Wadi Halfa","Amazon Retail","2026-07",953.85),
("Wadi Halfa","Amazon Retail","2026-08",998.15),
("Wadi Halfa","Ninja Retail","2026-08",6050.96),
]
# commission rate per brand on retail
RETAIL_RATE={"Marah":0.06,"SONDOS":0.06,"Wadi Halfa":0.04}

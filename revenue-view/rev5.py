# Fresh mcp_read.revenue pull 30 Aug 2026 (active brands, Nov 2025+): (brand, channel, ym, gmv, orders)
# Note: the Sonbol brand was renamed in the platform ("سنبل - المتجر الإلكتروني - Sonbol" -> "Sonbol").
# Sonbol rows here are pre-integration backfill and are EXCLUDED by build.py (from-integration figure in add6.py).
# Churned brands come from old_gmv.py (15 Aug snapshot — revenue view does not serve deactivated brands).
REV_ACT=[
("Arabesque","Salla","2026-05",109.25,1),("Arabesque","Salla","2026-06",383.53,3),("Arabesque","Salla","2026-07",1289.44,7),("Arabesque","Salla","2026-08",376.91,3),
("Arabesque","Trendyol","2026-05",2299.68,11),("Arabesque","Trendyol","2026-06",3559.06,18),("Arabesque","Trendyol","2026-07",3704.90,12),("Arabesque","Trendyol","2026-08",9763.38,50),
("Invita","Amazon","2025-11",7479.44,37),("Invita","Amazon","2025-12",9883.89,48),("Invita","Amazon","2026-01",9682.10,54),("Invita","Amazon","2026-02",19095.78,125),
("Invita","Amazon","2026-03",19579.02,127),("Invita","Amazon","2026-04",16941.30,127),("Invita","Amazon","2026-05",22888.68,110),("Invita","Amazon","2026-06",10251.25,57),
("Invita","Amazon","2026-07",12498.20,89),("Invita","Amazon","2026-08",13587.80,98),("Invita","Jahez","2026-03",132.00,1),("Invita","Jahez","2026-07",79.00,1),
("Invita","Noon","2025-11",5824.50,36),("Invita","Noon","2025-12",10642.50,58),("Invita","Noon","2026-01",11781.00,70),("Invita","Noon","2026-02",6210.48,41),
("Invita","Noon","2026-03",4496.25,27),("Invita","Noon","2026-04",3795.00,23),("Invita","Noon","2026-05",825.00,5),("Invita","Noon","2026-06",1155.00,5),
("Invita","Noon","2026-07",4265.00,27),("Invita","Noon","2026-08",10880.16,69),("Invita","Trendyol","2025-11",15144.20,83),("Invita","Trendyol","2025-12",9456.48,45),
("Invita","Trendyol","2026-01",8031.34,37),("Invita","Trendyol","2026-02",4749.63,23),("Invita","Trendyol","2026-03",8003.19,45),("Invita","Trendyol","2026-04",1542.73,8),
("Invita","Trendyol","2026-05",660.00,3),("Invita","Trendyol","2026-06",961.16,6),("Invita","Trendyol","2026-07",2867.08,16),("Invita","Trendyol","2026-08",264.72,2),
("Marah","Noon","2026-08",478.87,6),("Marah","Salla","2026-04",8389.84,18),("Marah","Salla","2026-05",4398.61,20),("Marah","Salla","2026-06",9995.03,26),
("Marah","Salla","2026-07",14094.94,55),("Marah","Salla","2026-08",3183.28,25),("Marah","Trendyol","2026-03",38.71,1),("Marah","Trendyol","2026-04",739.21,6),
("Marah","Trendyol","2026-05",6623.52,114),("Marah","Trendyol","2026-06",3488.84,63),("Marah","Trendyol","2026-07",1180.74,11),("Marah","Trendyol","2026-08",14593.77,269),
("Nokush","Amazon","2025-11",1830.40,41),("Nokush","Amazon","2025-12",1549.86,34),("Nokush","Amazon","2026-01",1133.21,21),("Nokush","Amazon","2026-02",3766.07,75),
("Nokush","Amazon","2026-03",3163.41,42),("Nokush","Amazon","2026-04",3290.10,49),("Nokush","Amazon","2026-05",4630.67,78),("Nokush","Amazon","2026-06",3952.03,58),
("Nokush","Amazon","2026-07",2668.25,34),("Nokush","Amazon","2026-08",1403.67,25),("Nokush","Noon","2025-11",56.95,1),("Nokush","Noon","2025-12",393.40,8),
("Nokush","Noon","2026-01",569.65,7),("Nokush","Noon","2026-02",829.45,10),("Nokush","Noon","2026-03",209.95,1),("Nokush","Noon","2026-04",1370.74,13),
("Nokush","Noon","2026-05",2807.69,44),("Nokush","Noon","2026-06",1353.00,20),("Nokush","Noon","2026-07",1892.50,30),("Nokush","Noon","2026-08",1434.39,27),
("Nokush","Salla","2025-11",777.45,6),("Nokush","Salla","2025-12",2172.19,10),("Nokush","Salla","2026-01",653.12,4),("Nokush","Salla","2026-02",953.57,5),
("Nokush","Salla","2026-03",855.08,5),("Nokush","Salla","2026-04",1241.39,5),("Nokush","Salla","2026-05",1236.82,6),("Nokush","Salla","2026-06",748.10,5),
("Nokush","Salla","2026-08",246.00,1),("Nokush","Trendyol","2025-11",2712.23,38),("Nokush","Trendyol","2025-12",287.74,10),("Nokush","Trendyol","2026-01",56.95,1),
("Nokush","Trendyol","2026-02",164.29,3),("Nokush","Trendyol","2026-03",342.83,7),("Nokush","Trendyol","2026-04",43.57,1),("Sense","Noon","2026-08",159.00,3),
("Sense","Salla","2026-04",2004.08,15),("Sense","Salla","2026-05",3751.67,27),("Sense","Salla","2026-06",2042.55,18),("Sense","Salla","2026-07",4879.35,25),
("Sense","Salla","2026-08",1314.77,14),("Sense","Trendyol","2026-05",1345.56,22),("Sense","Trendyol","2026-06",6588.79,135),("Sense","Trendyol","2026-07",803.54,12),
("Sense","Trendyol","2026-08",9480.90,192),("Sonbol","Salla","2026-02",376.20,1),("Sonbol","Salla","2026-06",683.00,2),("Sonbol","Salla","2026-07",320687.90,1060),
("Sonbol","Salla","2026-08",1059716.92,3709),("SONDOS","Jahez","2026-04",561.48,6),("SONDOS","Jahez","2026-06",324.85,1),("SONDOS","Noon","2026-05",2062.47,38),
("SONDOS","Noon","2026-06",5937.49,132),("SONDOS","Noon","2026-08",1429.94,16),("SONDOS","Salla","2026-03",217.60,1),("SONDOS","Salla","2026-04",24706.58,109),
("SONDOS","Salla","2026-05",48459.50,116),("SONDOS","Salla","2026-06",69284.01,160),("SONDOS","Salla","2026-07",199016.56,462),("SONDOS","Salla","2026-08",37023.19,131),
("SONDOS","Trendyol","2025-12",467.82,10),("SONDOS","Trendyol","2026-01",380.31,4),("SONDOS","Trendyol","2026-02",6088.50,114),("SONDOS","Trendyol","2026-03",2303.84,46),
("SONDOS","Trendyol","2026-04",4114.03,71),("SONDOS","Trendyol","2026-05",2628.82,36),("SONDOS","Trendyol","2026-06",2149.71,27),("SONDOS","Trendyol","2026-07",1269.98,19),
("SONDOS","Trendyol","2026-08",17603.48,229),("Wadi Halfa","Trendyol","2026-04",199.00,1),("Wadi Halfa","Trendyol","2026-05",534.25,2),("Wadi Halfa","Trendyol","2026-06",366.25,2),
("Wadi Halfa","Trendyol","2026-07",1200.15,7),("Wadi Halfa","Trendyol","2026-08",180.15,1),
]
# retained for build.py compatibility (retail now comes from po_plat.py — platform purchase orders)
PO=[]

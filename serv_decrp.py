services = {
			"cuisines`@`":
			{ 
		        "chinese`@`":
		        [
		      		"chowmein`@`",
		      		"manchurian`@`", 
		      		"hot and sour soup`@`",
		      		"spring rolls`@`",
		      		"dumplings or momos`@`",
		      		"chicken lollipop`@`",
		      		"american chop suey`@`",
		      		"szechwan`@`",
		      		"chilli chicken`@`",
		      		"prawn`@`",
		      		"fried rice`@`",
		      		"noodles`@`",
		      		"rice`@`"
		  	    ],
		  	    "maharashtrian`@`":
		  	    [
		      		"pav bhaji`@`",
		      		"misal pav`@`", 
		      		"kolhapuri vegetables`@`",
		      		"zunka bhakri`@`",
		      		"batata vada`@`",
		      		"pudachi wadi`@`",
		      		"kaju kothimbir vadi`@`",
		      		"aamti`@`",
		      		"pooran poli`@`",
		      		"bharleli vangi`@`"
		      	 ],
		      	 "punjabi`@`":
		      	[
		      		"butter chicken`@`",
		      		"sarson ka saag aur makki ki roti`@`",
		      		"tandoori chicken`@`",
		      		"chole bhature`@`",
		      		"masala channa`@`",
		      		"dal makhani`@`",
		      		"machchli amritsari`@`",
		      		"dhaba dal`@`",
		      		"paneer tikka`@`",
		      		"murgh malaiwala`@`"
		      	]
      		},
      		"appliance_repair`@`":
      		{
      			"kitchen`@`":
		        [
		      		"gas oven`@`",
		      		"electric oven`@`", 
		      		"dish washer`@`",
		      		"refrigerator`@`",
		      		"mixer grinder`@`",
		      		"water heater`@`",
		      		"water leakage`@`",
		      		"water leaking`@`",
		      		"cabinate refacing`@`"
		  	    ],
		  	    "household_electrical`@`":
		  	    [
		      		"washing machine`@`",
		      		"sump pump`@`", 
		      		"air conditioner`@`",
		      		"water cooler`@`",
		      		"fan`@`",
		      		"light`@`",
		      		"wire electric wiring`@`"
		      	],
		      	"household_water`@`":
		      	[
		      		"pipe fitting`@`",
		      		"seavage`@`",
		      		"overhead tank`@`",
		      		"water proofing`@`"
		      	],
		      	"computer`@`":
		      	[
		      	   "monitor`@`",
		      	   "cpu`@`",
		      	   "laptop`@`",
		      	   "notebook`@`",
		      	   "router`@`",
		      	   "hub`@`"
		      	]
      		},
      		"medical`@`":
      		{
      			"accident`@`":
		        [
		      		"first aid`@`",
		      		"cut`@`", 
		      		"blood`@`",
		      		"burn`@`",
		      		"injured`@`",
		      		"greviously injured`@`",
		      		"fracture`@`",
		      		"unconscious`@`",
		      		"vomitting`@`",
		      		"hurt`@`",
		      		"cramp`@`"
		  	    ]
      		},
      		"vehicle_repair`@`":
      		{
      			"MCWG`@`":
		        [
		      		"bike`@`",
		      		"scooty`@`", 
		      		"scooter`@`",
		      		"geared bike`@`",
		      		"hero honda`@`",
		      		"pulsar`@`",
		      		"bajaj`@`",
		      		"activa`@`",
		      		"motorcycle`@`"
		  	    ],
		  	    "LMV`@`":
		  	    [
		      		"car`@`",
		      		"suv`@`", 
		      		"sedan`@`",
		      		"hash back`@`",
		      		"maruti`@`",
		      		"hundai`@`",
		      		"tata`@`"
		      	]
      		},
      		"booking`@`":
      		{
      			"car`@`":
		        [
		      		"hatch back`@`",
		      		"sedan`@`", 
		      		"pooled car`@`",
		      		"long distance`@`",
		      		"cab`@`"	      		
		  	    ],
		  	    "bus`@`":
		  	    [
		      		"ac bus`@`",
		      		"Non ac bus`@`",
		      		"state transport`@`",
		      		"neeta`@`",
		      		"shivnerari`@`"
		      	]
      		}
  		}

def match_serv_menu(itemName):
	import re
	itemName2=itemName+"`@`"
	some_list=["no value"]
	index=0
	for service_type_key,service_descp_values in services.items(): #food,chinese
		for service_descp_key,service_descp_menu in service_descp_values.items(): #chinese,[]
			if itemName2.lower() in service_descp_key:
				index =0
				return (True,service_descp_key,service_descp_menu,index)
			if itemName2.lower() in service_descp_menu:
				return (True,service_type_key,service_descp_key,(service_descp_menu.index(itemName2)))
			if itemName2.lower() in service_type_key:
				z=services
				return (True,service_descp_key,[q for x,y in z.items() for q,w in y.items() if x==itemName2.lower()],0)
	else:
		return (False,some_list,some_list,index)
#print(match_serv_menu("uchowmein"))

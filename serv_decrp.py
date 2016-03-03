services = {
			"food":
			{ 
		        "chinese":
		        [
		      		"chowmein",
		      		"manchurian", 
		      		"hot and sour soup",
		      		"spring rolls",
		      		"dumplings or momos",
		      		"chicken lollipop",
		      		"american chop suey",
		      		"szechwan",
		      		"chilli chicken",
		      		"prawn",
		      		"fried rice",
		      		"noodles",
		      		"rice"
		  	    ],
		  	    "maharashtrian":
		  	    [
		      		"pav bhaji",
		      		"misal pav", 
		      		"kolhapuri vegetables",
		      		"zunka bhakri",
		      		"batata vada",
		      		"pudachi wadi",
		      		"kaju kothimbir vadi",
		      		"aamti",
		      		"pooran poli",
		      		"bharleli vangi"
		      	 ],
		      	 "punjabi":
		      	[
		      		"butter chicken",
		      		"sarson ka saag aur makki ki roti",
		      		"tandoori chicken",
		      		"chole bhature",
		      		"masala channa",
		      		"dal makhani",
		      		"machchli amritsari",
		      		"dhaba dal",
		      		"paneer tikka",
		      		"murgh malaiwala"
		      	]
      		},
      		"appliance_repair":
      		{
      			"kitchen":
		        [
		      		"gas oven won't heat",
		      		"electric oven won't heat", 
		      		"dish washer",
		      		"refrigerator",
		      		"mixer grinder",
		      		"water heater",
		      		"water leakage",
		      		"cabinate refacing"
		  	    ],
		  	    "household_electrical":
		  	    [
		      		"washing machine",
		      		"sump pump", 
		      		"air conditioner",
		      		"water cooler",
		      		"fan",
		      		"light",
		      		"wire electric wiring"
		      	],
		      	"household_water":
		      	[
		      		"pipe fitting",
		      		"seavage",
		      		"overhead tank",
		      		"water proofing"
		      	],
		      	"computer":
		      	[
		      	   "monitor",
		      	   "cpu",
		      	   "laptop",
		      	   "notebook",
		      	   "router",
		      	   "hub"
		      	]
      		}
  		}

def match_serv_menu(itemName):
	some_list=["no value"]
	for service_type_key,service_descp_values in services.items(): #food,chinese
		for service_descp_key,service_descp_menu in service_descp_values.items(): #chinese,[]
			if itemName in service_descp_key:
				return (True,service_descp_key,service_descp_menu)
			if itemName in service_descp_menu:
				return (True,service_type_key,service_descp_key)
	return (False,some_list,some_list)

#print(match_serv_menu("chinese"))
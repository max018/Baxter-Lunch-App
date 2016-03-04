var days = [
	{	"holiday": null, 
		"order": {
			"restaurant": "Zen Chinese Bistro",
			"option": "Pork Fried Rice"
		}
	},

	{	"holiday": "New Year's Eve", 
		"order": null
	},

	{	"holiday": "New Year's Day", 
		"order": null
	},

	{	"holiday": null, 
		"order": {
			"restaurant": "Portland Pie",
			"option": "Pizza: Cheese, Cheese"
		}
	},	

	{	"holiday": null, 
		"order": null
	},	
];


var dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

for(var i = 0; i  < days.length; i++){

	var day = days[i];

	var dayName = dayNames[i];

	if(day.order){
		console.log(dayName + ": " + day.order.restaurant + ' - ' + day.order.option)
	}

	if(day.holiday != null){
		console.log(dayName + ": " + day.holiday)	
	}

}
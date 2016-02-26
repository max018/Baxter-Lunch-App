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

console.log(days);

var monday = days[0];

var tuesday = days[1];

console.log(monday);

console.log(monday.order);

console.log(monday.order.restaurant + ' - ' + monday.order.option)



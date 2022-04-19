

function single_creation_update_phases(number_of_phases)
{
	var txt="";
	for (let i = 1; i <=number_of_phases; i++) 
	{
	fieldName="o"+i.toString();	
	fieldVal=document.forms["form"][fieldName].value;
	if (fieldVal!= null && fieldVal!= "")
		{
			if (i!=number_of_phases)
				txt+="'"+fieldName+"'"+":"+"'"+fieldVal+"'"+",";
			else
				txt+="'"+fieldName+"'"+":"+"'"+fieldVal+"'";
		}
	}
	document.forms["form"]["phases_names"].value=txt;
}
	





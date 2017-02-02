from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import *




function startind_5_details(players) {
	three_points_abilities="";
	two_points_abilities="";
	defense_abilities="";
	three_points_abilities="";
	one_on_one_abilities="";

	three_points_average=0;
	two_points_average=0;
	defense_average=0;
	one_on_one_average=0;

	var startind_5_details=[]

	for(var i=0;i<5;i++){
		three_points_average=three_points_average+players[i].three_points;
		two_points_average=three_points_average+players[i].two_points;
		defense_average=three_points_average+players[i].defense;
		one_on_one_average=three_points_average+players[i].one_on_one;
	}

	if (three_points_average>=8){
		three_points_abilities="High chance for thre.";
	}
	else if(three_points_average>4 && three_points_average<8){
		three_points_abilities="Mediume chance for three.";
	}
	else{
		three_points_abilities="Low chance for three.";
	}


	if (two_points_average>=8){
		three_points_abilities="high chance for two points.";
	}
	else if(two_points_average>4 && two_points_average<8){
		three_points_abilities="mediume chance for two points.";
	}
	else{
		three_points_abilities="low chance for two points.";
	}

	if (defense_average>=8){
		defense_abilities="very good defense.";
	}
	else if(defense_average>4 && defense_average<8){
		defense_abilities="good defense.";
	}
	else{
		defense_abilities="bad defense.";
	}

	if (one_on_one_average>=8){
		one_on_one_abilities="very good one on one abilities.";
	}
	else if(one_on_one_average>4 && one_on_one_average<8){
		one_on_one_abilities="good one on one abilities.";
	}
	else{
		one_on_one_abilities="bad one on one abilities.";
	}

	startind_5_details.push(defense_abilities);
	startind_5_details.push(one_on_one_abilities);
	startind_5_details.push(two_points_abilities);
	startind_5_details.push(three_points_abilities);

	return startind_5_details;

}





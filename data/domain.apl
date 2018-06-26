
domain{

	types{ Location, Victim, Robot }

	world{

		// Global Parameters
		numeric		DriveStd				();
		numeric		NominalCost				();
		numeric		NominalTimeMean			();
		numeric		NominalTimeStd			();
		numeric		TriageTimeMean			();
		numeric		TriageTimeStd			();

		// Robot types
		predicate	Rescuer					(Robot);
		predicate	Ambulance				(Robot);
		predicate	Bulldozer				(Robot);
		predicate	Transport				(Robot);

		// Roads
		predicate	Road					(Location,Location);
		numeric		Distance				(Location,Location);

		// Velocities
		numeric		RobotVelocity			(Robot);
	}

	state{
		function	Location	PosVictim	(Victim);
		function	Location	PosRobot	(Robot);
		function	Victim		RobotLoad	(Robot);
		function	Robot		Inside		(Robot);
		predicate	Busy					(Robot);
		predicate	Triaged					(Victim);
		predicate	Blocked					(Location);
	}


	// ====================================================
	// Actions
	// ====================================================

	action DriveFast(Robot r, Location orig, Location dest){
		duration:
			normal Distance(orig,dest)/RobotVelocity(r) DriveStd()*Distance(orig,dest)/RobotVelocity(r);
		cost:
			constant NominalCost();
		conditions:
			@start: PosRobot(r) = orig;
			@start: Road(orig, dest);
			@overall: !Blocked(orig);
			@overall: !Blocked(dest);
			@start: !Busy(r);
		effects:
			@start: Busy(r);
			@end: !Busy(r);
			@end: PosRobot(r) = dest;
	}

	action DriveSlow(Robot r, Location orig, Location dest){
		duration:
			normal 5.0*Distance(orig,dest)/RobotVelocity(r) DriveStd()*Distance(orig,dest)/RobotVelocity(r);
		cost:
			constant NominalCost();
		conditions:
			@start: PosRobot(r) = orig;
			@start: Road(orig, dest);
			@start: !Busy(r);
		effects:
			@start: Busy(r);
			@end: !Busy(r);
			@end: PosRobot(r) = dest;
	}

	action Clear(Robot r, Location l){
		duration:
			normal NominalTimeMean() NominalTimeStd();
		cost:
			constant NominalCost();
		conditions:
			@start: PosRobot(r) = l;
			@start: Bulldozer(r);
			@start: Blocked(l);
		effects:
			@end: !Blocked(l);
	}

	action Triage(Robot r, Victim v, Location l){
		duration:
			normal TriageTimeMean() TriageTimeStd();
		cost:
			constant NominalCost();
		conditions:
			@overall: PosRobot(r) = l;
			@overall: PosVictim(v) = l;
			@start: Rescuer(r);
			@start: !Busy(r);
		effects:
			@start: Busy(r);
			@end: !Busy(r);
			@end: Triaged(v);
	}

	action Load(Robot a, Robot r, Victim v, Location l){
		duration:
			normal NominalTimeMean() NominalTimeStd();
		cost:
			constant NominalCost();
		conditions:
			@overall: PosRobot(a) = l;
			@overall: PosRobot(r) = l;
			@overall: PosVictim(v) = l;
			@start: RobotLoad(a) = undefined;
			@start: Triaged(v);
			@start: Ambulance(a);
			@start: Rescuer(r);
			@start: r != a;
			@start: !Busy(r);
		effects:
			@start: Busy(r);
			@end: !Busy(r);
			@end: PosVictim(v) = undefined;
			@end: RobotLoad(a) = v;
	}

	action Unload(Robot a, Victim v, Location l){
		duration:
			normal NominalTimeMean() NominalTimeStd();
		cost:
			constant NominalCost();
		conditions:
			@overall: PosRobot(a) = l;
			@start: RobotLoad(a) = v;
			@start: PosVictim(v) = undefined;
			@start: Ambulance(a);
		effects:
			@end: PosVictim(v) = l;
			@end: RobotLoad(a) = undefined;
	}

	action EnterTransport(Robot r, Robot t, Location l){
		duration:
			normal NominalTimeMean() NominalTimeStd();
		cost:
			constant NominalCost();
		conditions:
			@start: !Busy(t);
			@overall: Inside(r) = undefined;
			@overall: PosRobot(t) = l;
			@overall: PosRobot(r) = l;
			@start: Transport(t);
			@start: Rescuer(r);
			@start: t != r;
		effects:
			@start: Busy(t);
			@end: !Busy(t);
			@end: PosRobot(r) = undefined;
			@end: Inside(r) = t;
	}

	action ExitTransport(Robot r, Robot t, Location l){
		duration:
			normal NominalTimeMean() NominalTimeStd();
		cost:
			constant NominalCost();
		conditions:
			@start: !Busy(t);
			@overall: PosRobot(t) = l;
			@start: Transport(t);
			@start: Rescuer(r);
			@start: t != r;
			@start: Inside(r) = t;
		effects:
			@start: Busy(t);
			@end: !Busy(t);
			@end: PosRobot(r) = l;
			@end: Inside(r) = undefined;
	}

}


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

}

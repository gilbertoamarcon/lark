Problem{
	Objects{
		Victim v0, v1, v2;
		Robot r0, r1;
		Robot a;
		Robot b;
		Location l0, l1, l2, l3;
	}
	WorldState{

		// Global Parameters
		DriveStd() = 0.2;
		NominalCost() = 0.1;

		// Timing parameters
		NominalTimeMean() = 0.1;
		NominalTimeStd() = 0.1;
		TriageTimeMean() = 0.4;
		TriageTimeStd() = 0.2;

		// Roads
		Road(l0,l1); Road(l1,l0); Distance(l0,l1) = 50.0; Distance(l1,l0) = 50.0;
		Road(l0,l2); Road(l2,l0); Distance(l0,l2) = 10.0; Distance(l2,l0) = 10.0;
		Road(l2,l3); Road(l3,l2); Distance(l2,l3) = 10.0; Distance(l3,l2) = 10.0;

		// Velocities
		RobotVelocity(r0) = 5.0;
		RobotVelocity(r1) = 5.0;
		RobotVelocity(a) = 30.0;
		RobotVelocity(b) = 10.0;

		// Robot types
		Rescuer		(r0);
		Rescuer		(r1);
		Ambulance	(a);
		Bulldozer	(b);

	}
	InitialState{

		// Victim Positions
		PosVictim(v0)=l2;
		PosVictim(v1)=l1;
		PosVictim(v2)=l3;

		// Robot Positions
		PosRobot(r0)=l0;
		PosRobot(r1)=l0;
		PosRobot(a)=l0;
		PosRobot(b)=l0;

		// Road Blocks
		Blocked(l2);

	}
	Goal{
		PosVictim(v0)==l0;
		PosVictim(v1)==l0;
		PosVictim(v2)==l0;
	}
}

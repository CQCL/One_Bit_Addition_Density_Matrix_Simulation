OPENQASM 2.0;
include "qelib1.inc";

gate dephasing_noise(theta) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
{
rz(theta) q1;
rz(theta) q2;
rz(theta) q3;
rz(theta) q4;
rz(theta) q5;
rz(theta) q6;
rz(theta) q7;
rz(theta) q8;
rz(theta) q9;
rz(theta) q10;
}

// quadratic_dephasing_rate=0.122
gate idle_2q q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
{
//dephasing_noise(0.00035624) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
//dephasing_noise(0.0027414) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
dephasing_noise(0.0) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
}

gate idle_1q q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
{
//dephasing_noise(0.00015616) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
//dephasing_noise(0.0001202) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
dephasing_noise(0.0) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
}

gate idle_measurement q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
{
//dephasing_noise(0.000074054) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
//dephasing_noise(0.0005699) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
dephasing_noise(0.0) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
}

gate average_transport_noise q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
{

// 2 pi x sqrt (3/2) x 0.122 x 3 x 10^-4
// dephasing_noise(0.0002816) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
// 2 pi x sqrt (3/2) x 0.122 x 10^-3
//dephasing_noise(0.0009389) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
// 2 pi x sqrt (3/2) x 0.122 x 0.0057
//dephasing_noise(0.005351) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
dephasing_noise(0.0) q1,q2,q3,q4,q5,q6,q7,q8,q9,q10;
}

// idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
// idle_measurement q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
// idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
// average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

qreg q[8];
qreg a[2]; 
creg c[14]; 

h q[0];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

h q[1];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

h q[2];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

h q[6];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

cx q[0],q[4];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

cx q[1],q[5];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

cx q[2],q[3];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

cx q[6],q[7];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx q[0],q[1];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

cx q[1],q[2];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx q[2],q[0];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx q[1],q[6];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

cx q[6],q[0];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx q[0],q[1];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

h a[1];

idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

cx q[4],a[0];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx a[1],q[1];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx q[1],a[0];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx a[1],q[4];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx q[3],a[0];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx a[1],q[6];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];



cx a[1],q[3];
idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


cx q[6],a[0];

idle_2q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];


h a[1];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

t q[0];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

tdg q[1];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

tdg q[2];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

t q[3];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

tdg q[4];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

t q[5];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

t q[6];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];

tdg q[7];
idle_1q q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];
average_transport_noise q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],a[0],a[1];



// No second half of circuit


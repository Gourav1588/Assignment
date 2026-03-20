
// add the data structure for the program calculation.
const students = [
    {
        name: "Lalit",
        marks: [
            { subject: "Math", score: 78 },
            { subject: "English", score: 82 },
            { subject: "Science", score: 74 },
            { subject: "History", score: 69 },
            { subject: "Computer", score: 88 }
        ],
        attendance: 82
    },
    {
        name: "Rahul",
        marks: [
            { subject: "Math", score: 90 },
            { subject: "English", score: 85 },
            { subject: "Science", score: 80 },
            { subject: "History", score: 76 },
            { subject: "Computer", score: 92 }
        ],
        attendance: 91
    },
    {
        name: "Aman",
        marks: [
            { subject: "Math", score: 50 },
            { subject: "English", score: 55 },
            { subject: "Science", score: 60 },
            { subject: "History", score: 58 },
            { subject: "Computer", score: 62 }
        ],
        attendance: 70
    }
];



// Function for Total Marks Calculation


function calculateTotalMarks(studentList) {
    console.log("Total Marks:");
    studentList.forEach(student => {
        let sum = 0;
        student.marks.forEach(item => {
            sum += item.score;
        });
        student.totalMarks = sum;
        console.log(`${student.name} Total Marks: ${student.totalMarks}`);
    });
    console.log("\n")

}
calculateTotalMarks(students);


// Function for Average Marks Calculation


function calculateAverageMarks(studentList) {
    console.log("Average Marks for Each Student");
    studentList.forEach(student => {

        student.averageMarks = student.totalMarks / student.marks.length;
        console.log(`${student.name} Average: ${student.averageMarks.toFixed(1)}`);
        "\n"
    });
    console.log("\n");
}

// calling function


calculateAverageMarks(students);

// function to calculate subject-wise highest marks
function SubjectHighest(students) {

    const subjectData = {};

    students.forEach(student => {

        student.marks.forEach(mark => {

            // // if subject is encountered first time, initialize it
            if (!subjectData[mark.subject]) {
                subjectData[mark.subject] = {
                    highest: mark.score,
                    topper: student.name
                };
            } else {
                // it compare the highest mark and then put the new value
                if (mark.score > subjectData[mark.subject].highest) {
                    subjectData[mark.subject].highest = mark.score;
                    subjectData[mark.subject].topper = student.name;
                }
            }

        });

    });

    return subjectData;
}
const highestMarks = SubjectHighest(students);

console.log("\nSubject-wise Highest Marks:");

for (let subject in highestMarks) {
    console.log(
        `${subject}: ${highestMarks[subject].topper} (${highestMarks[subject].highest})`
    );
}
console.log("\n");


// function to calculate subject-wise average
function getSubjectAverage(students) {
    console.log("Subject-wise Average:");

    const subjectData = {};

    students.forEach(student => {

        student.marks.forEach(mark => {

            // if subject is seen first time
            if (!subjectData[mark.subject]) {
                subjectData[mark.subject] = {
                    total: mark.score,
                    count: 1
                };
            } else {
                // add score and increase count
                subjectData[mark.subject].total += mark.score;
                subjectData[mark.subject].count++;
            }

        });

    });

    return subjectData;
}


const results = getSubjectAverage(students);

for (let subject in results) {
    const avg = results[subject].total / results[subject].count;

    console.log(`Average ${subject} Score: ${avg.toFixed(1)}`);

}
console.log("\n");



// function to find class topper
function getClassTopper(studentList) {

    let highest = 0;
    let topper = "";

    studentList.forEach(student => {

        if (student.totalMarks > highest) {
            highest = student.totalMarks;
            topper = student.name;
        }

    });

    console.log("\nClass Topper:");
    console.log(`Class Topper: ${topper} with ${highest} marks`);
    console.log("\n")
 }
 getClassTopper(students);


function assignGrade(studentList) {
    console.log("Student Grades:");
    studentList.forEach(student => {

        // calculating the average
        const avg = student.totalMarks / student.marks.length;

        let grade = "";

        // if any student has less than 40 marks it should be fail.
        let failedSubject = "";
        student.marks.forEach(mark => {
            if (mark.score <= 40) {
                failedSubject = mark.subject;
            }
        });


        if (failedSubject) {
            grade = `Fail (Failed in ${failedSubject})`;
        }
        else if (student.attendance < 75) {
            grade = "Fail (Low Attendance)";
        }
        else {
            // if student have averege marks greater than 85 it should get A grade and other are mentioned.
            if (avg >= 85) grade = "A";
            else if (avg >= 70) grade = "B";
            else if (avg >= 50) grade = "C";
            else grade = "Fail";
        }

        console.log(`${student.name}`);
        console.log(`Average: ${avg.toFixed(2)}`);
        console.log(`Grade: ${grade}`);
        console.log("\n")
    });
}


assignGrade(students);
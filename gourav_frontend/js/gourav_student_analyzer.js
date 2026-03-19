
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
//console.log(students);


// Function for Total Marks Calculation


function calculateTotalMarks(studentList) {
    studentList.forEach(student => {
        let sum = 0;
        student.marks.forEach(item => {
            sum += item.score;
        });
        student.totalMarks = sum; 
        console.log(`${student.name} Total Marks: ${student.totalMarks}`);
    });
}

// Function for Average Marks Calculation


function calculateAverageMarks(studentList) {
    studentList.forEach(student => {
        
            student.averageMarks = student.totalMarks / student.marks.length;
            console.log(`${student.name} Average: ${student.averageMarks.toFixed(1)}`);
    });
}

// calling function
// calculateTotalMarks(students);
// calculateAverageMarks(students);

// function to calculate subject-wise highest marks
function SubjectHighest(students) {

  const subjectData = {};

  students.forEach(student => {

    student.marks.forEach(mark => {

     // it works when the new subject arrive
      if (!subjectData[mark.subject]) {
        subjectData[mark.subject] = {
          highest: mark.score,
          topper: student.name
        };
      } else {
        // it comapres the higest mark and then put the new value
        if (mark.score > subjectData[mark.subject].highest) {
          subjectData[mark.subject].highest = mark.score;
          subjectData[mark.subject].topper = student.name;
        }
      }

    });

  });

  return subjectData;
}
// const highestMarks = SubjectHighest(students);

// console.log("\nSubject-wise Highest Marks:");

// for (let subject in highestMarks) {
//   console.log(
//     `${subject}: ${highestMarks[subject].topper} (${highestMarks[subject].highest})`
//   );
// }



// function to calculate subject-wise average
function getSubjectAverage(students) {

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
using Backend.Models;

namespace Backend.Data;

public static class DbInitialiser {
    public static void Initialise(DatabaseContext context) {
        // create database schema if none exists
        context.Database.EnsureCreated();

        // If there are already data in the database, don't add any more
        if (context.Users.Any() || context.Course.Any() || context.Question.Any() || context.Test.Any()) {
            return;
        }

        // Add some data to the database
        AnswerOption answer1 = new AnswerOption {Option = "Answer 1", IsCorrect = true};
        AnswerOption answer2 = new AnswerOption {Option = "Answer 2"};
        AnswerOption answer3 = new AnswerOption {Option = "Answer 3"};
        AnswerOption answer4 = new AnswerOption {Option = "Answer 4"};

        List<AnswerOption> answers = new List<AnswerOption> {
            answer1, answer2, answer3, answer4
        };

        context.AddRange(answers);

        Question question1 = new Question {Query = "Question 1", Options = new List<AnswerOption> { answer1, answer2, answer3, answer4 }};

        List<Question> questions = new List<Question> {
            question1
        };

        context.AddRange(questions);

        Test test1 = new Test {Questions = questions};

        Course math101 = new Course {Name = "Math 101"};
        Course math102 = new Course {Name = "Math 102"};
        Course math103 = new Course {Name = "Math 103"};

        List<Course> courses = new List<Course> {
            math101, math102, math103
        };

        context.AddRange(courses);

        List<User> users = new List<User> {
            new User {Username = "user1", Password = "pw1", EnrolledCourses = new HashSet<Course> { math101 }, Tests = new List<Test> { test1 } },
            new User {Username = "user2", Password = "pw2"},
            new User {Username = "user3", Password = "pw3"},
        };

        context.AddRange(users);

        context.SaveChanges();
    }
}
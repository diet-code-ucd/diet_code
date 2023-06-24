using Backend.Models;

namespace Backend.Data;

public static class DbInitialiser
{
    public static void Initialise(DatabaseContext context)
    {
        // create database schema if none exists
        context.Database.EnsureCreated();

        // If there are already data in the database, don't add any more
        if (context.Users.Any() || context.Courses.Any() || context.Questions.Any() || context.Tests.Any())
        {
            return;
        }

        // divide the answersList into 4 answer options for each newly created question
        List<Question> questionsList = new List<Question>();
        for (int i = 0; i < 12; i++)
        {
            Question question = new Question { 
                QuestionText = $"Question {i + 1}",
                Answer = $"Answer {i + 1}",
                Explanation = $"Explanation {i + 1}",
                Difficulty = Difficulty.Easy
            };
            questionsList.Add(question);
        }

        context.AddRange(questionsList);

        Test test1 = new Test { Questions = questionsList.GetRange(0, 5) };

        context.Add(test1);

        Course math101 = new Course { Name = "Math 101", Questions = questionsList };
        Course math102 = new Course { Name = "Math 102" };
        Course math103 = new Course { Name = "Math 103" };

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
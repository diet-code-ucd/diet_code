using System.Drawing.Text;
using System.Text.Json;
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

        // Read the json file containing the questions Data/combined_df.json
        string jsonString = File.ReadAllText("Data/combined_df.json");

        // Convert the json string to a list of Question objects
        List<Question> questions = JsonSerializer.Deserialize<List<Question>>(jsonString)!;
        context.AddRange(questions);

        Test test1 = new Test { Questions = questions.GetRange(0, 5) };

        context.Add(test1);

        Course maths = new Course { Name = "Maths", Questions = questions };
        Course physics = new Course { Name = "Physics", Questions = new List<Question>() };

        List<Course> courses = new List<Course> {
            maths,
              physics

        };

        context.AddRange(courses);

        List<User> users = new List<User> {
            new User {Username = "user1", Password = "pw1", DateOfBirth = DateTime.Parse("2010-05-06"), EnrolledCourses = courses, Tests = new List<Test> { test1 } },
            new User {Username = "user2", Password = "pw2", DateOfBirth = DateTime.Parse("1993-09-13")},
            new User {Username = "user3", Password = "pw3", DateOfBirth = DateTime.Parse("1987-11-19")},
        };

        context.AddRange(users);

        context.SaveChanges();
    }
}

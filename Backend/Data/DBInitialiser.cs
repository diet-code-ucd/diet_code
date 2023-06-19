using Backend.Models;

namespace Backend.Data;

public static class DbInitialiser {
    public static void Initialise(DatabaseContext context) {
        context.Database.EnsureCreated();

        Course math101 = new Course {Name = "Math 101"};
        Course math102 = new Course {Name = "Math 102"};
        Course math103 = new Course {Name = "Math 103"};

        List<Course> courses = new List<Course> {
            math101, math102, math103
        };

        context.AddRange(courses);

        List<User> users = new List<User> {
            new User {Username = "user1", Password = "pw1", EnrolledCourses = new List<Course> { math101 } },
            new User {Username = "user2", Password = "pw2"},
            new User {Username = "user3", Password = "pw3"},
        };

        context.AddRange(users);

        context.SaveChanges();
    }
}
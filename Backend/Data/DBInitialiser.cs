using Backend.Models;

namespace Backend.Data;

public static class DbInitialiser {
    public static void Initialise(DatabaseContext context) {
        context.Database.EnsureCreated();

        List<User> users = new List<User> {
            new User {Username = "user1", Password = "pw1"},
            new User {Username = "user2", Password = "pw2"},
            new User {Username = "user3", Password = "pw3"},
        };

        context.AddRange(users);

        context.SaveChanges();
    }
}
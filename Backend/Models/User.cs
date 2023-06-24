using System;
using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class User {
     //public int Id { get; set;}
     public string Username { get; set;}
     public string pwd { get; set;}
     //public virtual ICollection<Course>? EnrolledCourses { get; set;}
     //public virtual ICollection<Test>? Tests { get; set;}
}

public class AppDbContext : DbContext
{
    public DbSet<User> Users { get; set; }

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>().HasNoKey();
    }

    public static bool ValidateUserCredentials(string username, string password)
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlServer("your-connection-string")
            .Options;

        using (var dbContext = new AppDbContext(options))
        {
            var user = dbContext.Users.FirstOrDefault(u => u.Username == username && u.pwd == password);
            return user != null;
        }
    }

    //To check if the password and username is correct (Need to work on encryption)
    //bool isValid = ValidateUserCredentials(username, password);

    //    if (isValid)
    //    {
    //        Console.WriteLine("Login successful!");
    //    }
    //    else
    //    {
    //        Console.WriteLine("Invalid username or password.");
    //    }



}
using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class User {
     public int Id { get; set;}
     public string Username { get; set;}
     public string Password { get; set;}
     public ICollection<Course>? EnrolledCourses { get; set;}
     public ICollection<Test>? Tests { get; set;}
}
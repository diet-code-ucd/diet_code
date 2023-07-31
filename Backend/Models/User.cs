using System;
using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class User {
     public int Id { get; set;}
     public string Username { get; set;}
     public string Password { get; set;}
     public DateTime DateOfBirth { get; set;}
     public virtual ICollection<Course>? EnrolledCourses { get; set;}
     public virtual ICollection<Test>? Tests { get; set;}
}

namespace Backend.Models;

public class User {
     public int Id { get; set;}
     public string Username { get; set;}
     public string Password { get; set;}
     public ICollection<Course> EnrolledCourses { get; set;}
}

public class UserDTO {
     public int Id { get; set;}
     public string Username { get; set;}
     public ICollection<Course>? EnrolledCourses { get; set;}

     public static UserDTO Convert(User user) {
        return new UserDTO { 
            Id = user.Id,
            Username = user.Username,
            EnrolledCourses = user.EnrolledCourses,
        };
     }
}
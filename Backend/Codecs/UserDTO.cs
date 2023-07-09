using Backend.Models;

namespace Backend.Codecs;

public class UserDTO
{
    public int Id { get; set; }
    public string Username { get; set; }
    public string DateOfBirth { get; set; }
    public virtual ICollection<int>? EnrolledCourses { get; set; }
    public virtual ICollection<int>? Tests { get; set; }

    public static UserDTO FromUser(User user)
    {
        return new UserDTO
        {
            Id = user.Id,
            Username = user.Username,
            DateOfBirth = user.DateOfBirth.ToString("yyyy-MM-dd"),
            EnrolledCourses = user.EnrolledCourses?.Select(c => c.Id).ToList(),
            Tests = user.Tests?.Select(t => t.Id).ToList()
        };
    }
}

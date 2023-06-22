using Backend.Models;

namespace Backend.Codecs;

public class CourseDTO {
    public int Id { get; set;}
    public string Name { get; set;}
    public virtual ICollection<int>? Questions { get; set;}

    public static CourseDTO FromCourse(Course course) {
        return new CourseDTO {
            Id = course.Id,
            Name = course.Name,
            Questions = course.Questions?.Select(q => q.Id).ToList()
        };
    }
}
namespace Backend.Models;

public class Course {
    public int Id { get; set;}
    public string Name { get; set;}
    public virtual ICollection<Question>? Questions { get; set;}
}
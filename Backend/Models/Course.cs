namespace Backend.Models;

public class Course {
    public int Id { get; set;}
    public string Name { get; set;}
    public ICollection<Question>? Questions { get; set;}
}
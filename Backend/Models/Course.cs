namespace Backend.Models;

public class Course {
    public int Id { get; set;}
    public HashSet<Question> Questions { get; set; }
}
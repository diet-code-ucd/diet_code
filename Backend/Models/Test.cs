namespace Backend.Models;

public class Test {
    public int Id { get; set;}
    public virtual ICollection<Question> Questions { get; set;} = new List<Question>();
}
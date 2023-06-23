namespace Backend.Models;

public class Test {
    public int Id { get; set;}
    public virtual ICollection<Question> Questions { get; set;}
    public virtual ICollection<AnswerOption> Answers { get; set;}
}
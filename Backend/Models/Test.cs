namespace Backend.Models;

public class Test {
    public int Id { get; set;}
    public ICollection<Question> Questions { get; set;}
    public ICollection<AnswerOption> Answers { get; set;}
}
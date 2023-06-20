namespace Backend.Models;

public class Question
{
    public int Id { get; set; }
    public string QuestionText { get; set; }
    public virtual ICollection<AnswerOption> Options { get; set; }
}
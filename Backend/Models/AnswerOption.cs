namespace Backend.Models;

public class AnswerOption {
    public int Id { get; set;}
    public string Option { get; set;}
    public bool IsCorrect { get; set;} = false;
    public Question Question { get; set;}
}   
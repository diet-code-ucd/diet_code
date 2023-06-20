using Backend.Data;
using Microsoft.EntityFrameworkCore;
using Backend.Models;

namespace Backend.Models;

public class DatabaseContext : DbContext
{
    public DatabaseContext(DbContextOptions<DatabaseContext> options)
        : base(options)
    {
        DbInitialiser.Initialise(this);
    }   

    public DbSet<Backend.Models.User> Users { get; set; }  = default!;

    public DbSet<Backend.Models.Course> Course { get; set; } = default!;

    public DbSet<Backend.Models.Question> Question { get; set; } = default!;

    public DbSet<Backend.Models.Test> Test { get; set; } = default!;
}
using Backend.Data;
using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class DatabaseContext : DbContext
{
    public DatabaseContext(DbContextOptions<DatabaseContext> options)
        : base(options)
    {
        DbInitialiser.Initialise(this);
    }   

    public DbSet<User> Users { get; set; } = null!;
}
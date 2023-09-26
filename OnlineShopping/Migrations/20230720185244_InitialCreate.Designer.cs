﻿// <auto-generated />
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using OnlineShopping.Data;

#nullable disable

namespace OnlineShopping.Migrations
{
    [DbContext(typeof(DataContext))]
    [Migration("20230720185244_InitialCreate")]
    partial class InitialCreate
    {
        /// <inheritdoc />
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "7.0.9")
                .HasAnnotation("Relational:MaxIdentifierLength", 128);

            SqlServerModelBuilderExtensions.UseIdentityColumns(modelBuilder);

            modelBuilder.Entity("OnlineShopping.Model.Inventory", b =>
                {
                    b.Property<int>("ProductId")
                        .HasColumnType("int");

                    b.Property<int>("Quantity")
                        .HasColumnType("int");

                    b.HasKey("ProductId");

                    b.ToTable("Inventory");

                    b.HasData(
                        new
                        {
                            ProductId = 1,
                            Quantity = 10
                        },
                        new
                        {
                            ProductId = 2,
                            Quantity = 10
                        },
                        new
                        {
                            ProductId = 3,
                            Quantity = 10
                        },
                        new
                        {
                            ProductId = 4,
                            Quantity = 10
                        },
                        new
                        {
                            ProductId = 5,
                            Quantity = 10
                        },
                        new
                        {
                            ProductId = 6,
                            Quantity = 10
                        },
                        new
                        {
                            ProductId = 7,
                            Quantity = 10
                        },
                        new
                        {
                            ProductId = 8,
                            Quantity = 10
                        });
                });

            modelBuilder.Entity("OnlineShopping.Model.ProcessedCart", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<int>("CartId")
                        .HasColumnType("int");

                    b.Property<string>("Items")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<DateTime>("PaymentDate")
                        .HasColumnType("datetime2");

                    b.Property<decimal>("TotalAmount")
                        .HasColumnType("decimal(18,2)");

                    b.HasKey("Id");

                    b.ToTable("ProcessedCarts");
                });

            modelBuilder.Entity("OnlineShopping.Model.Products", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<string>("Image")
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("Name")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<decimal>("Price")
                        .HasColumnType("decimal(18,2)");

                    b.HasKey("Id");

                    b.ToTable("Products");

                    b.HasData(
                        new
                        {
                            Id = 1,
                            Image = "./images/hamburger.jpg",
                            Name = "Hamburger",
                            Price = 7.99m
                        },
                        new
                        {
                            Id = 2,
                            Image = "./images/cheeseburger.jpg",
                            Name = "Cheeseburger",
                            Price = 8.99m
                        },
                        new
                        {
                            Id = 3,
                            Image = "./images/tacos.jpg",
                            Name = "Tacos",
                            Price = 7.99m
                        },
                        new
                        {
                            Id = 4,
                            Image = "./images/chicken-sandwich.jpg",
                            Name = "Chicken Sandwish",
                            Price = 7.99m
                        },
                        new
                        {
                            Id = 5,
                            Image = "./images/fries.jpg",
                            Name = "Fries",
                            Price = 3.99m
                        },
                        new
                        {
                            Id = 6,
                            Image = "./images/cookies.jpg",
                            Name = "Cookies",
                            Price = 3.49m
                        },
                        new
                        {
                            Id = 7,
                            Image = "./images/soda.jpg",
                            Name = "Soda",
                            Price = 1.99m
                        },
                        new
                        {
                            Id = 8,
                            Image = "./images/draft.jpg",
                            Name = "Draft Beer",
                            Price = 5.99m
                        });
                });

            modelBuilder.Entity("OnlineShopping.Models.Cart", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<string>("Name")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.HasKey("Id");

                    b.ToTable("Carts");
                });

            modelBuilder.Entity("OnlineShopping.Models.CartItem", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<int>("CartId")
                        .HasColumnType("int");

                    b.Property<int>("ProductId")
                        .HasColumnType("int");

                    b.Property<string>("ProductName")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<int>("Quantity")
                        .HasColumnType("int");

                    b.Property<decimal>("Value")
                        .HasColumnType("decimal(18,2)");

                    b.HasKey("Id");

                    b.HasIndex("CartId");

                    b.ToTable("CartItem");
                });

            modelBuilder.Entity("OnlineShopping.Model.Inventory", b =>
                {
                    b.HasOne("OnlineShopping.Model.Products", "Product")
                        .WithOne()
                        .HasForeignKey("OnlineShopping.Model.Inventory", "ProductId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Product");
                });

            modelBuilder.Entity("OnlineShopping.Models.CartItem", b =>
                {
                    b.HasOne("OnlineShopping.Models.Cart", "Cart")
                        .WithMany("Items")
                        .HasForeignKey("CartId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Cart");
                });

            modelBuilder.Entity("OnlineShopping.Models.Cart", b =>
                {
                    b.Navigation("Items");
                });
#pragma warning restore 612, 618
        }
    }
}

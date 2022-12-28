# Project 'TaXCalC' for Itemis

This project arose from an Itemis challenge and began on December 28, 2022, at 5.45 p.m.
This readme 'documentation' clarifies how the challenge was addressed and why certain assumptions were made.

## I. Constrains by Itemis
Itemis first established six constraints for the challenge:
1. Use a GitHub git repository for code distribution
2. Send an email with the link or zip file to the local git repository
3. Focus on code quality and create production-ready code
4. Work in a test-driven style
5. Commit changes
6. Mark assumptions made

## II. Challenge description
Given the [constraints](#i-constrains-by-itemis), the following challenge needed to be solved:

> ## Problem 1: SALES TAXES
> Basic sales tax is applicable at a rate of 10% on all goods, except books, food, and medical products that are exempt.
> Import duty is an additional sales tax  applicable on all imported goods at a rate of 5%, with no exemptions.
> When I purchase items I receive a receipt which lists the name of all the items and their price (including tax),
> finishing with the total cost of the items, and the total amounts of sales taxes paid.
> The rounding rules for sales tax are that for a tax rate of n%, a shelf price of p contains
> (np/100 rounded up to the nearest 0.05) amount of sales tax.
>
> Write an application that prints out the receipt details for these shopping baskets...
> 
> ### INPUT:
> 
> #### Input 1:
> - 1 book at 12.49
> - 1 music CD at 14.99
> - 1 chocolate bar at 0.85
> 
> #### Input 2:
> - 1 imported box of chocolates at 10.00
> - 1 imported bottle of perfume at 47.50
> 
> #### Input 3:
> - 1 imported bottle of perfume at 27.99
> - 1 bottle of perfume at 18.99
> - 1 packet of headache pills at 9.75
> - 1 box of imported chocolates at 11.25
>
> ### OUTPUT:
> 
> #### Output 1:
> - 1 book: 12.49
> - 1 music CD: 16.49
> - 1 chocolate bar: 0.85
> - Sales Taxes: 1.50
> - Total: 29.83
> 
> #### Output 2:
> - 1 imported box of chocolates: 10.50
> - 1 imported bottle of perfume: 54.65
> - Sales Taxes: 7.65
> - Total: 65.15
> #### Output 3:
> - 1 imported bottle of perfume: 32.19
> - 1 bottle of perfume: 20.89
> - 1 packet of headache pills: 9.75
> - 1 imported box of chocolates: 11.85
> - Sales Taxes: 6.70
> - Total: 74.68

## III. Requirements
Based on the challenge description in [chapter II.](#ii-challenge-description), the requirements of TaXCalC must be
identified in order to implement the correct software product. For the requirement specification, the template
provided by Pohl and Rupp [\[1, pp. 71–75\]](#a-bibliography) is used.

| Req. ID | Requirements Specification | Source
| ------- | -------------------------- | ------
| REQ 1 | The SYSTEM SHALL BE ABLE TO apply a 10% tax rate on all goods, except books, food, and medical products | "Basic sales tax is applicable at a rate of 10% on all goods, except books, food, and medical products that are exempt." [\[Itemis challenge description, sentence 1\]](#ii-challenge-description)
| REQ 2 | The SYSTEM SHALL BE ABLE TO apply a 5% import duty on imported goods | "Import duty is an additional sales tax applicable on all imported goods at a rate of 5%, with no exemptions." [\[Itemis challenge description, sentence 2\]](#ii-challenge-description)
| REQ 3 | The SYSTEM SHALL PROVIDE the user WITH THE ABILITY to see the receipt which lists the name of all items and their single taxed price | "When I purchase items I receive a receipt which lists the name of all the items and their price (including tax) \[...\]" [\[Itemis challenge description, sentence 3\]](#ii-challenge-description)
| REQ 4 | The SYSTEM SHALL PROVIDE the user WITH THE ABILITY to see the receipt which lists, besides REQ 3, the total cost of the items, and the total amount of sales taxes | "\[...\] finishing with the total cost of the items, and the total amounts of sales taxes paid." [\[Itemis challenge description, sentence 3\]](#ii-challenge-description)
| REQ 5 | The SYSTEM SHALL calculate the sales tax with the following formular: `n*p/100`; for a tax rate of `n%` and a price of `p` | "The rounding rules for sales tax are that for a tax rate of n%, a shelf price of p contains (np/100 rounded up to the nearest 0.05) amount of sales tax." [\[Itemis challenge description, sentence 4\]](#ii-challenge-description)

## A. Bibliography
1. Klaus Pohl and Chris Rupp, "Basiswissen Requirements Engineering: Ausund Weiterbildung nach IREB-Standard zum
Certified Professional for Requirements Engineering Foundation Level", in 5th ed., ser. iSQI-Reihe.
Heidelberg, Germany: dpunkt.verlag, 2021.
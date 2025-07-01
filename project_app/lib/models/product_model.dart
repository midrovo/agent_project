class Product {
  final int id;
  final String name;
  final String? image;
  final String description;
  final double stock;
  final double listPrice;
  final double standardPrice;
  final double discount;

  Product({
    required this.id,
    required this.name,
    this.image,
    required this.description,
    required this.stock,
    required this.listPrice,
    required this.standardPrice,
    required this.discount,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      name: json['name'],
      image: json['image'],
      description: json['description'],
      stock: (json['stock'] as num).toDouble(),
      listPrice: (json['list_price'] as num).toDouble(),
      standardPrice: (json['standard_price'] as num).toDouble(),
      discount: (json['discount'] as num).toDouble(),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:project_app/models/product_model.dart';
import 'package:project_app/services/product_service.dart';

class ProductListScreen extends StatelessWidget {
  final ProductService service = ProductService();

  ProductListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: Text(
          'Productos',
          style: TextStyle(
            color: Colors.black87,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: FutureBuilder<List<Product>>(
        future: service.fetchProducts(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No se encontraron productos.'));
          }

          final products = snapshot.data!;
          return ListView.builder(
            itemCount: products.length,
            itemBuilder: (context, index) {
              final product = products[index];
              return ProductCard(product: product);
            },
          );
        },
      ),

    );
  }
}


class ProductCard extends StatelessWidget {
  final Product product;

  const ProductCard({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20.0),
      child: Container(
        margin: const EdgeInsets.only(top: 30, bottom: 30),
        width: double.infinity,
        decoration: _cardBorder(),
        child: Column(
          children: [
            Stack(
              children: [
                _BackgroundImage(urlImage: product.image),
                Positioned(
                  top: 0,
                  right: 0,
                  child: _PriceTag(
                    priceProduct: product.listPrice,
                    discountProduct: product.discount,
                    standardPrice: product.standardPrice,
                  ),
                ),
                if (product.stock == 0)
                  const Positioned(
                    top: 0,
                    left: 0,
                    child: _NotAvailable(),
                  ),
              ],
            ),
            _ProductDetails(
              nameProduct: product.name,
              description: product.description,
            ),
            const SizedBox(height: 10),
          ],
        ),
      ),
    );
  }

  BoxDecoration _cardBorder() => BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(25),
    boxShadow: const [
      BoxShadow(
        color: Colors.black26,
        blurRadius: 10,
        offset: Offset(0, 5),
      )
    ],
  );
}



class _BackgroundImage extends StatelessWidget {
  final String? urlImage;

  const _BackgroundImage({this.urlImage});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.vertical(top: Radius.circular(25)),
      child: urlImage != null
          ? Image.network(
        urlImage!,
        height: 300,
        width: double.infinity,
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) => Container(
          color: Colors.grey[300],
          alignment: Alignment.center,
          child: const Icon(Icons.broken_image, size: 80),
        ),
      )
          : Container(
        height: 300,
        width: double.infinity,
        color: Colors.grey[300],
        alignment: Alignment.center,
        child: const Icon(Icons.image_not_supported, size: 80),
      ),
    );
  }
}


class _ProductDetails extends StatelessWidget {
  final String nameProduct;
  final String description;

  const _ProductDetails({
    required this.nameProduct,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 15.0, vertical: 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            nameProduct,
            style: const TextStyle(
              color: Colors.black87,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 5),
          Text(
            description,
            style: const TextStyle(
              color: Colors.black54,
              fontSize: 12,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}



class _PriceTag extends StatelessWidget {
  final double priceProduct;
  final double discountProduct;
  final double standardPrice;

  const _PriceTag({
    required this.priceProduct,
    required this.discountProduct,
    required this.standardPrice,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: Colors.green[700],
        borderRadius: const BorderRadius.only(
          topRight: Radius.circular(25),
          bottomLeft: Radius.circular(25),
        ),
      ),
      child: discountProduct > 0
          ? Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            '\$${priceProduct.toStringAsFixed(2)}',
            style: const TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(width: 5),
          Text(
            '\$${standardPrice.toStringAsFixed(2)}',
            style: const TextStyle(
              color: Colors.white70,
              fontSize: 12,
              decoration: TextDecoration.lineThrough,
            ),
          ),
        ],
      )
          : Text(
        '\$${priceProduct.toStringAsFixed(2)}',
        style: const TextStyle(
          color: Colors.white,
          fontSize: 16,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}


class _NotAvailable extends StatelessWidget {
  const _NotAvailable();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: Colors.red[700],
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(25),
          bottomRight: Radius.circular(25),
        ),
      ),
      child: const Text(
        'Sin Stock',
        style: TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}



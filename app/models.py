class Opinion:
    def __init__(
        self,
        opinion_id="",
        author="",
        recommendation="",
        score="",
        content="",
        pros=None,
        cons=None,
        helpful="0",
        unhelpful="0",
        publish_date="",
        purchase_date=""
    ):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.score = score
        self.content = content
        self.pros = pros if pros is not None else []
        self.cons = cons if cons is not None else []
        self.helpful = helpful
        self.unhelpful = unhelpful
        self.publish_date = publish_date
        self.purchase_date = purchase_date

    def to_dict(self):
        return {
            "opinion_id": self.opinion_id,
            "author": self.author,
            "recommendation": self.recommendation,
            "score": self.score,
            "content": self.content,
            "pros": self.pros,
            "cons": self.cons,
            "helpful": self.helpful,
            "unhelpful": self.unhelpful,
            "publish_date": self.publish_date,
            "purchase_date": self.purchase_date
        }


class Product:
    def __init__(self, product_id, product_name="", opinions=None, stats=None):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions if opinions is not None else []
        self.stats = stats if stats is not None else {}

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions": [opinion.to_dict() for opinion in self.opinions],
            "stats": self.stats
        }
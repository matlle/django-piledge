<?php
    
class DemoController extends controller {

    public function topArticlesAction($num) {
        $articles = '';

        return $this->render('topArticle.html.twig', array('articles' => $articles,));
    }

}

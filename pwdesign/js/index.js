$(function() {

    //CONTROLE DE TAMANHO DOS SELETORES, NÚMERO DE CLICKS NOS BOTÕES DE "PRÓXIMO" E "ANTERIOR"
    var select_brand = $('#select_brand'),
        select_storage = $('#select_storage'),
        select_processor = $('#select_processor'),
        sel_next_button = $('#sel_next_button'),
        sel_prev_button = $('#sel_prev_button'),
        sel_width = 300,
        sel_border_size = 12,
        sel_padding = 20,
        clicks = 0,
        selectors_lenght = $('.selectors').length;

    //CONTROLE DAS FUNÇÕES QUE O BOTÃO "PRÓXIMO" DEVERÁ EXERCER
    sel_next_button.click(function() {

        //BLOQUEAR A PASSAGEM PARA O PRÓXIMO SE HÁ CAMPOS OBRIGATÓRIOS
        var checkboxes_brand = document.getElementsByName("brand"),
            brand_ok = false;

        for (var i = 0; i < checkboxes_brand.length; i++) {
            if (checkboxes_brand[i].checked) {
                brand_ok = true;
                break;
            }
        }

        if (brand_ok)
            select_brand.css("margin-left", "-" + getTotal("next") + "px");
        else
            alert("Preencha no mínimo uma marca!");
    });

    //BOTÃO "ANTERIOR" NÃO POSSUI MUITOS CONTROLES, APENAS DEVE EXERCER A FUNÇÃO DE VOLTAR PARA ETAPAS ANTERIORES DE ACORDO COM A VONTADE DO USUÁRIO
    sel_prev_button.click(function() {
        select_brand.css("margin-left", "-" + getTotal("prev") + "px");
    });

    //CONTROLA O TOTAL EM INTEIRO QUE SERÁ CONVERTIDO EM PIXELS, QUE UM SELETOR DEVE SE MOVER, COM BASE NO TAMANHO DA DIV SELETORA, NO PADDING
    //QUE ELA CONTÉM, E NAS SUAS BORDAS... ALÉM DE MULTIPLICAR ISSO PELO NÚMERO DE VEZES QUE O USUÁRIO CLICOU EM ALGUM BOTÃO
    function getTotal(type) {
        if (type == "next" && clicks < (selectors_lenght - 1))
            clicks++;
        else if (type == "prev" && clicks > 0)
            clicks--;

        return ((clicks * sel_width) + (clicks * sel_border_size) + (clicks * (sel_padding * 2)));
    }

});
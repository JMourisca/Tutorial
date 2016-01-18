/**
 * Created by juliana on 16/01/16.
 */
app.service("Data", ["$http", function ($http) {
    var obj = {};

    obj.get = function (q, cache) {
        cache = cache || false;
        return $http.get(q, {cache: cache}).then(function (results) {
            return results.data;
        });
    };
    obj.post = function (q, object) {
        return $http.post(q, object).then(function (results) {
            return results.data;
        });
    };
    obj.put = function (q, object) {
        return $http.put(q, object).then(function (results) {
            return results.data;
        });
    };
    obj.delete = function (q) {
        return $http.delete(q).then(function (results) {
            return results.data;
        });
    };

    return obj;
}]).controller("CategoryController", ["Data", "$window", "notify", function (Data, $window, notify) {
    var cat = this;

    cat.delete = function(type, id){
        Data.delete("/" + type + "/" + id).then(function (response) {
            if(response.result === "True") {
                notify({message: response.msg, classes: "alert-success"});
                 $window.location.reload();
            } else {
                notify({message: response.msg, classes: "alert-danger"});
                console.log(response.msg);
            }
        });
    };
}]).controller("PhotosController", ["Data", function (Data) {
    var pt = this;

    pt.getPhotos = function (id) {
        Data.get("/album/" + id + "/photos").then(function (response) {
            pt.photos = response;
        });
    };

    pt.select = function (photo) {
        console.log(photo.id);
        photo.active = !photo.active;
    };
}]);